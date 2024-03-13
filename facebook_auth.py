# import requests
# import uvicorn
# from facebook_business import FacebookAdsApi
# from facebook_business.adobjects.adaccount import AdAccount
# from facebook_business.adobjects.adsinsights import AdsInsights
# from facebook_business.adobjects.campaign import Campaign
# from fastapi import FastAPI
# from fastapi.security import OAuth2AuthorizationCodeBearer
# from flask import session, request, redirect, url_for, Flask
# # from flask import Flask, redirect, url_for, session, request
# from flask_oauthlib.client import OAuth
# from facebook_business.adobjects.adaccountuser import AdAccountUser as AdUser
# # import uvicorn
# # from fastapi.testclient import TestClient
# # app = Flask(__name__)
# # app.secret_key = 'supersecretkey'
# # from fastapi import FastAPI
#
# # app = FastAPI()
# class FacebookAuth:
#     def __init__(self, app_id, app_secret):
#         self.app = FastAPI()
#         self.app.secret_key = 'supersecretkey'
#         self.oauth = OAuth(self.app)
#
#         self.app.oauth2_scheme = self.oauth
#
#         # Замените значения YOUR_APP_ID и YOUR_APP_SECRET на значения из вашего Facebook App
#         facebook = self.oauth.remote_app(
#             'facebook',
#             consumer_key=app_id,
#             consumer_secret=app_secret,
#             request_token_params={'scope': 'email'},
#             base_url='https://graph.facebook.com',
#             request_token_url=None,
#             access_token_method='POST',
#             access_token_url='/oauth/access_token',
#             authorize_url='https://www.facebook.com/dialog/oauth'
#         )
#
#         @self.app.get('/')
#         def index():
#             return '''Добро пожаловать! <a href="/login">Войти с использованием Facebook</a>'''
#
#         @self.app.get('/login')
#         def login():
#             return facebook.authorize(callback=url_for('authorized', _external=True))
#         @self.app.get('/logout')
#         def logout():
#             session.pop('facebook_token', None)
#             return redirect(url_for('index'))
#         @self.app.get('/login/authorized')
#         def authorized():
#             response = facebook.authorized_response()
#             if response is None or response.get('access_token') is None:
#                 return 'Доступ запрещен: причина = {}, ошибка = {}'.format(
#                     request.args['error_reason'],
#                     request.args['error_description']
#                 )
#             session['facebook_token'] = (response['access_token'], '')
#             user_data = facebook.get('/me')
#             return 'Добро пожаловать, {}'.format(user_data.data['name'])
#         @facebook.tokengetter
#         def get_facebook_oauth_token():
#             return session.get('facebook_token')
#
#     def run(self):
#         uvicorn.run(self.app, host="localhost", port=5000, ssl_keyfile='C:\\Users\Professional\\Downloads\\openssl-3.2.0\\openssl-3.2.0\\demos\\sslecho\\key.pem',
#                                                             ssl_certfile='C:\\Users\Professional\\Downloads\\openssl-3.2.0\\openssl-3.2.0\\demos\\sslecho\\cert.pem')
import json
import secrets
from typing import List, Dict
from urllib.parse import unquote

import facebook
import facebook_business
import uvicorn
from django.db import router
from facebook_business import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adsinsights import AdsInsights
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.serverside import user_data
# def campaign_data(self, app_id, app_secret):
    #     if 'facebook_token' not in session:
    #         # Если токен отсутствует, можно вернуть ошибку или поддерживать перенаправление на страницу авторизации
    #         return None
    #
    #     access_token = session['facebook_token'][0]
    #     FacebookAdsApi.init(app_id, app_secret, access_token)
    #     me = AdUser(fbid='me')
    #     my_accounts = list(me.get_ad_accounts(fields=[AdAccount.Field.name]))
    #
    #     if not my_accounts:
    #         # Если у пользователя нет рекламных аккаунтов, вернуть ошибку или поддерживать создание аккаунта
    #         return None
    #
    #     my_account = my_accounts[0]
    #     CampaignName = my_account.get_campaigns(fields=[Campaign.Field.name])
    #
    #     fields = [
    #         AdsInsights.Field.adset_name,
    #         AdsInsights.Field.ad_name,
    #         AdsInsights.Field.spend,
    #         AdsInsights.Field.impressions,
    #         AdsInsights.Field.date_start,
    #         AdsInsights.Field.date_stop,
    #         AdsInsights.Field.campaign_name,
    #         AdsInsights.Field.dda_results,
    #         AdsInsights.Field.cpm,
    #         AdsInsights.Field.impressions
    #     ]
    #
    #     mas = []
    #     for i in CampaignName:
    #         campdata = i.get_insights(params={
    #             'level': 'adset',
    #             'date_preset': 'this_month',
    #             'time_increment': 1
    #         }, fields=fields)
    #         mas.append(campdata)
    #
    #     # Возвращаем данные о кампаниях
    #     return mas

    # def run(self):
    #     self.app.run(debug=True, host='localhost', port=5000, ssl_context=(
    #         'C:\\Users\Professional\\Downloads\\openssl-3.2.0\\openssl-3.2.0\\demos\\sslecho\\cert.pem',
    #         'C:\\Users\Professional\\Downloads\\openssl-3.2.0\\openssl-3.2.0\\demos\\sslecho\\key.pem'
    #     ))

from fastapi import FastAPI, Request, Form, Query
from facebook_business.adobjects.adaccountuser import AdAccountUser as AdUser
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adsinsights import AdsInsights
import httpx
from fastapi.logger import logger
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from pandas import DataFrame
from facebook_business.adobjects.campaign import Campaign
from starlette.middleware.sessions import SessionMiddleware

from google_sheets import GoogleSheet


app = FastAPI()
secret_key = secrets.token_urlsafe(32)
app.add_middleware(SessionMiddleware, secret_key=secret_key)
templates = Jinja2Templates(directory="templates")
class FacebookAuth():
    def __init__(self, client_id, client_secret, redirect_uri, scope):
        self.client_id = '935313657940273'
        self.client_secret = '468a6b379ca39d558b3df1f0769eab17'
        self.redirect_uri = redirect_uri
        self.scope = scope

    async def read_root(request: Request):
        return templates.TemplateResponse("index.html", {"request": request})

    async def login(request: Request):
        client_id = '935313657940273'
        redirect_uri = "https://facebookservice.onrender.com/login/callback"
        scope = "email"
        authorization_url = (
            "https://www.facebook.com/dialog/oauth?"
            f"client_id={client_id}&"
            f"redirect_uri={redirect_uri}"
        )
        return RedirectResponse(url=authorization_url)

    async def select_fields(request: Request, my_company: str = Query(..., alias="campaign")):
        fields = [
            AdsInsights.Field.adset_name,
            AdsInsights.Field.ad_name,
            AdsInsights.Field.spend,
            AdsInsights.Field.impressions,
            AdsInsights.Field.date_start,
            AdsInsights.Field.date_stop,
            AdsInsights.Field.campaign_name,
            AdsInsights.Field.dda_results,
            AdsInsights.Field.cpm
        ]
        return templates.TemplateResponse("select_fields.html", {"request": request, "fields": fields, "my_account": my_company})

    async def compaign_data(request: Request, fields: List[str] = Query(..., alias="fields"), my_account: str = Query(..., alias="my_account")):
        mas = []
        campaign = Campaign(fbid=my_account)
        custom_time_range = json.dumps({'since': '2023-01-01', 'until': '2023-12-31'})

        campdata = campaign.get_insights(params={
            'level': 'adset',
            'time_range': custom_time_range,
            'time_increment': 1
        }, fields=fields)

        mas.append(campdata)

        camp_name_data = []
        camp_name_spend = []
        camp_date_start = []
        camp_date_stop = []
        camp_compaign = []
        camp_cpm = []
        camp_impressions = []

        for f in mas:
            for j in f:
                camp_name_data.append(j.get("adset_name", None))
                camp_name_spend.append(j.get("spend", None))
                camp_date_start.append(j.get("date_start", None))
                camp_date_stop.append(j.get("date_stop", None))
                camp_compaign.append(j.get("campaign_name", None))
                camp_cpm.append(j.get("cpm", None))
                camp_impressions.append(j.get("impressions", None))

        df = DataFrame()
        df["Date_start"] = camp_date_start
        df["Date_stop"] = camp_date_stop
        df["Spend"] = camp_name_spend
        df["Name"] = camp_name_data
        df["Compaign"] = camp_compaign
        df["CPM"] = camp_cpm
        df["Impressions"] = camp_impressions

        gs = GoogleSheet()

        test_range = 'test!A:G'

        df_json = df.values.tolist()
        test_values = df_json
        gs.append_values(test_range, test_values)

        return ("successful")

    async def login_callback(code: str = Form(...)):
        token_url = "https://graph.facebook.com/v19.0/oauth/access_token"
        client_id = '935313657940273'
        client_secret = '468a6b379ca39d558b3df1f0769eab17'
        redirect_uri = "https://facebookservice.onrender.com/login/callback"
        token_data = {
            "code": code,
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri,
        }

        async with httpx.AsyncClient() as client:
            token_response = await client.post(token_url, data=token_data)
            token_response.raise_for_status()
            token_data = token_response.json()

        token = token_data["access_token"]


        redirect_url = f"https://facebookservice.onrender.com/login/callback/select_account?token={token}"
        return RedirectResponse(url=redirect_url, status_code=307)

    async def select_account(request: Request, token: str):
        request.session["token"] = token

        FacebookAdsApi.init('323958937015510', '4017320d9d5dcc49869874e73904b872', token)
        me = AdUser(fbid='me')
        my_accounts = list(me.get_ad_accounts(fields=[AdAccount.Field.name]))
        return templates.TemplateResponse("select_account.html", {"request": request, "my_accounts": my_accounts})

    async def select_compaign(request: Request, account: str = Form(...)):
        # Пример: Получение списка компаний выбранного аккаунта
        selected_account = AdAccount(account)
        campaignss = []
        campaigns = selected_account.get_campaigns(fields=[Campaign.Field.id, Campaign.Field.name])
        fields = [AdsInsights.Field.ad_name]
        custom_time_range = json.dumps({'since': '2023-01-01', 'until': '2023-12-31'})
        for compaing in campaigns:
            field = compaing.get_insights(params={
                'level': 'adset',
                'time_range': custom_time_range,
                'time_increment': 1
            }, fields=fields)
            insights_list = list(field)
            if insights_list:
                campaignss.append(compaing)
        return templates.TemplateResponse("select_compaign.html", {"request": request, "compaigns": campaignss})

    # def run(self):
    #     uvicorn.run(app, host="localhost", port=5000,
    #             ssl_keyfile='C:\\Users\Professional\\Downloads\\openssl-3.2.0\\openssl-3.2.0\\demos\\sslecho\\key.pem',
    #             ssl_certfile='C:\\Users\Professional\\Downloads\\openssl-3.2.0\\openssl-3.2.0\\demos\\sslecho\\cert.pem')

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return await FacebookAuth.read_root(request)

@app.get("/login")
async def login(request: Request):
    return await FacebookAuth.login(request)

@app.get("/login/callback")
async def login_callback(code: str = Query(...)):
    result = await FacebookAuth.login_callback(code)
    return result

@app.get("/login/callback/select_account", response_class=HTMLResponse)
async def select_account(request: Request, token: str):
    return await FacebookAuth.select_account(request, token)

@app.get("/login/callback/select_compaign", response_class=HTMLResponse)
async def select_compaign(request: Request,  account: str = Query(..., alias="my_account_id")):
    return await FacebookAuth.select_compaign(request, account)

@app.get("/login/callback/select_fields", response_class=HTMLResponse)
async def select_fields(request: Request, my_company: str = Query(..., alias="campaign")):
    return await FacebookAuth.select_fields(request, my_company)

@app.get("/login/compaign")
async def compaign_data(request: Request, fields: List[str] = Query(..., alias="fields"), my_account: str = Query(..., alias="my_account")):
    result = await FacebookAuth.compaign_data(request, fields, my_account)
    return result

