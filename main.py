# import sys
# import webbrowser
# #
# import facebook
# import facebook_business.bootstrap
# import requests
# from django.http import HttpRequest, HttpResponse
# from django.shortcuts import render
# from Naked.toolshed.shell import execute_js, muterun_js
# from flask import Flask, redirect, url_for, session, request
# from flask_oauthlib.client import OAuth
# from facebook_business.api import FacebookAdsApi
# from facebook_business.adobjects.adaccount import AdAccount
# from facebook_business.adobjects.adsinsights import AdsInsights
# from facebook_business.adobjects.campaign import Campaign
# import telebot;
# from telebot import types
# from facebook_business.adobjects.adaccountuser import AdAccountUser as AdUser
# from pandas import DataFrame
# import os.path
# import os.path
# import pickle
# from googleapiclient.discovery import build
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request
# class GoogleSheet:
#   SPREADSHEET_ID = '1Q_FhA_Og0_5aZLQHNLq1JJnpcsIgqvgDW1mWa0q6kXY'
#   SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
#   service = None
#
#   def __init__(self):
#     creds = None
#     if os.path.exists('token.pickle'):
#       with open('token.pickle', 'rb') as token:
#         creds = pickle.load(token)
#
#     if not creds or not creds.valid:
#       if creds and creds.expired and creds.refresh_token:
#         creds.refresh(Request())
#       else:
#         print('flow')
#         flow = InstalledAppFlow.from_client_secrets_file(
#           'credentials.json', self.SCOPES)
#         creds = flow.run_local_server(port=0)
#       with open('token.pickle', 'wb') as token:
#         pickle.dump(creds, token)
#
#     self.service = build('sheets', 'v4', credentials=creds)
#
#   def updateRangeValues(self, range, values):
#     data = [{
#       'range': range,
#       'values': values
#     }]
#     body = {
#       'valueInputOption': 'USER_ENTERED',
#       'data': data
#     }
#     result = self.service.spreadsheets().values().batchUpdate(spreadsheetId=self.SPREADSHEET_ID, body=body).execute()
#     print('{0} cells updated.'.format(result.get('totalUpdatedCells')))
#
# def auth():
#     app = Flask(__name__)
#     app.secret_key = 'supersecretkey'
#
#     oauth = OAuth(app)
#
#     # Замените значения YOUR_APP_ID и YOUR_APP_SECRET на значения из вашего Facebook App
#     facebook = oauth.remote_app(
#         'facebook',
#         consumer_key='323958937015510',
#         consumer_secret='4017320d9d5dcc49869874e73904b872',
#         request_token_params={'scope': 'email'},
#         base_url='https://graph.facebook.com',
#         request_token_url=None,
#         access_token_method='POST',
#         access_token_url='/oauth/access_token',
#         authorize_url='https://www.facebook.com/dialog/oauth'
#     )
#
#     @app.route('/')
#     def index():
#         return 'Добро пожаловать! <a href="/login">Войти с использованием Facebook</a>'
#
#     @app.route('/login')
#     def login():
#         return facebook.authorize(callback=url_for('authorized', _external=True))
#
#     @app.route('/logout')
#     def logout():
#         session.pop('facebook_token', None)
#         return redirect(url_for('index'))
#
#     @app.route('/login/authorized')
#     def authorized():
#         response = facebook.authorized_response()
#
#         if response is None or response.get('access_token') is None:
#             return 'Доступ запрещен: причина = {}, ошибка = {}'.format(
#                 request.args['error_reason'],
#                 request.args['error_description']
#             )
#
#         session['facebook_token'] = (response['access_token'], '')
#         user_data = facebook.get('/me')
#
#         return 'Добро пожаловать, {}'.format(user_data.data['name'])
#
#     @facebook.tokengetter
#     def get_facebook_oauth_token():
#         return session.get('facebook_token')
#     print(get_facebook_oauth_token())
#
#     app.run(debug=True, host='localhost', port=5000, ssl_context=(
#         'C:\\Users\Professional\\Downloads\\openssl-3.2.0\\openssl-3.2.0\\demos\\sslecho\\cert.pem',
#         'C:\\Users\Professional\\Downloads\\openssl-3.2.0\\openssl-3.2.0\\demos\\sslecho\\key.pem'))
# def main(df):
#
#   gs = GoogleSheet()
#   fs = auth()
#
#   # print(fs)
#   test_range = 'test!A:G'
#   df_json = df.values.tolist()
#   test_values = df_json
#   gs.updateRangeValues(test_range, test_values)
#
# my_access_token = 'EAAEmo5Fc1NYBOzZCbfBnqJFoYmGqJqpE1T469qTP4yo9JdH3Cyt60JVWZACvQXiA6qu0wIY4ILgFAQP83kLJvpLMoUYMQma0vFuDci6Vknk6JNHY01Ae458HIVAA3eWXNduARbZAZBsSMdUZBp7qhLs7SescIqaChUSCZAhbxuBMvLdPNg84ghQAvj3aOwvwCgy4KB'
# my_app_id = '323958937015510'
# my_app_secret = '4017320d9d5dcc49869874e73904b872'
# FacebookAdsApi.init(my_app_id, my_app_secret, my_access_token)
# me = AdUser(fbid='me')
# my_accounts = list(me.get_ad_accounts(fields=[AdAccount.Field.name]))
# my_account = my_accounts[0]
# CampaignName = my_account.get_campaigns(fields=[
#     Campaign.Field.name,
# ])
# fields = [
#     AdsInsights.Field.adset_name,
#     AdsInsights.Field.ad_name,
#     AdsInsights.Field.spend,
#     AdsInsights.Field.impressions,
#     AdsInsights.Field.date_start,
#     AdsInsights.Field.date_stop,
#     AdsInsights.Field.campaign_name,
#     AdsInsights.Field.dda_results,
#     AdsInsights.Field.cpm,
#     AdsInsights.Field.impressions]
# mas = []
# for i in CampaignName:
#     campdata = i.get_insights(params=
#                               {'level': 'adset',
#                                'date_preset': 'this_month',
#                                'time_increment': 1},
#                               fields=fields)
#     mas.append(campdata)
# camp_name_data = []
# camp_name_spend = []
# camp_date_start = []
# camp_date_stop = []
# camp_compaign = []
# # camp_result = []
# camp_cpm = []
# camp_impressions = []
# for f in mas:
#     for j in f:
#         camp_name_data.append(j['adset_name'])
#         camp_name_spend.append(j['spend'])
#         camp_date_start.append(j['date_start'])
#         camp_date_stop.append(j['date_stop'])
#         camp_compaign.append(j['campaign_name'])
#         # camp_result.append(j['dda_results'])
#         camp_cpm.append(j['cpm'])
#         camp_impressions.append(j['impressions'])
# df = DataFrame()
# df['Date_start'] = camp_date_start
# df['Date_stop'] = camp_date_stop
# df['Spend'] = camp_name_spend
# df['Name'] = camp_name_data
# df['Compaign'] = camp_compaign
# # df['Result'] = camp_result
# df['CPM'] = camp_cpm
# df['Impressions'] = camp_impressions
# main(df)
# bot = telebot.TeleBot('6713056294:AAFAr-2ipWydHjlsiXgKPuxGI-YmeGStvOQ');
#
#
# @bot.message_handler(commands=['start'])
# def start(message):
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     btn1 = types.KeyboardButton("👋 Начать работу с нами")
#     btn2 = types.KeyboardButton("❓ Узнать подробнее о сервисе")
#     markup.add(btn1, btn2)
#     bot.send_message(message.chat.id,
#                      text="Здравствуйте, {0.first_name}! Вас приветствует сервис отчетности таргета".format(
#                          message.from_user), reply_markup=markup)
#
#
# @bot.message_handler(content_types=['text'])
# def func(message):
#     if message.text == "/start":
#         main(df)
#     back = types.KeyboardButton("Вернуться в главное меню")
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     if (message.text == "👋 Начать работу с нами"):
#
#         btn1 = types.KeyboardButton("Предоставить доступ к своей отчетности Facebook ADS")
#         markup.add(btn1)
#         bot.send_message(message.chat.id,
#                          text="Уважаемый, {0.first_name}! Нам нужен доступ к вашей отчетности Facebook".format(
#                              message.from_user), reply_markup=markup)
#     elif (message.text == "Предоставить доступ к своей отчетности Facebook ADS"):
#         btn1 = types.KeyboardButton("Предоставить доступ")
#         markup.add(btn1)
#         auth()
#         bot.send_message(message.chat.id, text="перейдите по ссылке: {0.link}".format(auth()), reply_markup=markup)
#     # elif (message.text == "Предоставить доступ"):
#
#     elif (message.text == "❓ Узнать подробнее о сервисе"):
#         bot.send_message(message.char.id, text="Наш сервис занимается ")
#         btn1 = types.KeyboardButton("Как меня зовут?")
#         btn2 = types.KeyboardButton("Что я могу?")
#         markup.add(btn1, btn2, back)
#         bot.send_message(message.chat.id, text="Задай мне вопрос", reply_markup=markup)
#
#     else:
#         bot.send_message(message.chat.id, text="На такую команду я не запрограммировал..")
import asyncio
import threading

import uvicorn
from fastapi import FastAPI, Form, Request
# bot.polling(none_stop=True, interval=0)
# from flask import Flask, url_for, request
from social_core.backends.facebook import FacebookOAuth2
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

# from flask import Flask
#
from telegram_bot import TelegramBot
from facebook_auth import FacebookAuth
from google_sheets import GoogleSheet
from pandas import DataFrame

my_app_id = '323958937015510'
my_app_secret = '4017320d9d5dcc49869874e73904b872'
fs = FacebookAuth(my_app_id, my_app_secret, "http://localhost:5000/login/callback", "email")
bot = TelegramBot()
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# def run_telegram_bot():
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    # loop.run_until_complete(bot.run())
# @app.get("/", response_class=HTMLResponse)
# async def read_root(request: Request):
#     return await fs.read_root(request)
#
# @app.get("/login")
# async def login(request: Request):
#     return await fs.login(request)
#
# @app.get("/login/callback")
# async def login_callback():
#     result = await fs.login_callback()
#     return result
fs.run()
# def main(loop=None):
#     my_access_token = 'EAAEmo5Fc1NYBOzZCbfBnqJFoYmGqJqpE1T469qTP4yo9JdH3Cyt60JVWZACvQXiA6qu0wIY4ILgFAQP83kLJvpLMoUYMQma0vFuDci6Vknk6JNHY01Ae458HIVAA3eWXNduARbZAZBsSMdUZBp7qhLs7SescIqaChUSCZAhbxuBMvLdPNg84ghQAvj3aOwvwCgy4KB'
#
#     # telegram_bot_thread = threading.Thread(target=run_telegram_bot)
#     # telegram_bot_thread.start()
#
#     # Запустите FastAPI
#     fs.run()
#
# if __name__ == "__main__":
#     main()
    # Остальной код для инициализации данных и запуска бота
    # loop = asyncio.get_event_loop()
    # loop.create_task(fs.run())
    # loop.create_task(bot.run_polling())
    # loop.run_forever()
    # my_access_token = 'EAAEmo5Fc1NYBOzZCbfBnqJFoYmGqJqpE1T469qTP4yo9JdH3Cyt60JVWZACvQXiA6qu0wIY4ILgFAQP83kLJvpLMoUYMQma0vFuDci6Vknk6JNHY01Ae458HIVAA3eWXNduARbZAZBsSMdUZBp7qhLs7SescIqaChUSCZAhbxuBMvLdPNg84ghQAvj3aOwvwCgy4KB'
    # my_app_id = '323958937015510'
    # my_app_secret = '4017320d9d5dcc49869874e73904b872'
    # fs = FacebookAuth(my_app_id, my_app_secret, "http://localhost:5000/login/callback", "email")
    # fs.run()
    # Получаем событийный цикл
    # try:
    #     loop = asyncio.get_event_loop()
    # # Запускаем функцию main в цикле событий
    # except RuntimeError as e:
    #     if "There is no current event loop" in str(e):
    #         # Если цикла нет, создаем новый
    #         loop = asyncio.new_event_loop()
    #         asyncio.set_event_loop(loop)
    #     else:
    #         raise
    #
    # loop.run_until_complete(main())
    # fs.run()

    # gs = GoogleSheet()

    # Получение данных с Facebook API
    # campaign_data = fs.campaign_data(my_app_id, my_app_secret)
    # # Создание DataFrame
    # df = DataFrame(campaign_data)

    # main(df)

    # bot = TelegramBot(fs, "6713056294:AAFAr-2ipWydHjlsiXgKPuxGI-YmeGStvOQ")

    # fs.run()  # Запуск аутентификации Facebook
    # bot.run_polling()  # Запуск телеграм-бота
    # bot.run_polling()

# import webbrowser
# from flask import Flask, send_from_directory
#
# html_content = """
# <script>
#     // Ваш JavaScript-код здесь
# </script>
# """
#
# with open('your_file.html', 'w') as f:
#     f.write(html_content)
# html_content = """
# <script>
#     (function(d, s, id){
#         var js, fjs = d.getElementsByTagName(s)[0];
#         if (d.getElementById(id)) {return;}
#         js = d.createElement(s); js.id = id;
#         js.src = "https://connect.facebook.net/en_US/sdk.js";
#         fjs.parentNode.insertBefore(js, fjs);
#     }(document, 'script', 'facebook-jssdk'));
#
#     window.fbAsyncInit = function() {
#         FB.init({
#             appId: '323958937015510',
#             xfbml: true,
#             version: 'v18.0'
#         });
#
#         FB.login(function(response) {
#             if (response.authResponse) {
#                 console.log('Welcome!  Fetching your information.... ');
#                 FB.api('/me', {fields: 'name, email'}, function(response) {
#                     document.getElementById("profile").innerHTML = "Good to see you, " + response.name + ". I see your email address is " + response.email;
#                 });
#             } else {
#                 console.log('User cancelled login or did not fully authorize.');
#             }
#         });
#     };
# </script>
# """
#
# with open('your_file.html', 'w') as f:
#     f.write(html_content)
#
# app = Flask(__name__)
#
# @app.route('/')
# def index():
#     return send_from_directory('.', 'your_file.html')  # Замените 'your_file.html' на имя вашего HTML-файла
#
#
# if __name__ == '__main__':
#     app.run(debug=True, host='localhost', port=5000, ssl_context=(
#         'C:\\Users\Professional\\Downloads\\openssl-3.2.0\\openssl-3.2.0\\demos\\sslecho\\cert.pem',
#         'C:\\Users\Professional\\Downloads\\openssl-3.2.0\\openssl-3.2.0\\demos\\sslecho\\key.pem'))

# import requests
# from flask import Flask, request, jsonify
#
# def exchange_code_for_token(app_id, app_secret, code):
#     token_exchange_url = f"https://graph.facebook.com/v18.0/oauth/access_token"
#     params = {
#         'client_id': app_id,
#         'client_secret': app_secret,
#         'code': code,
#         'redirect_uri': 'https://localhost:5000/login/authorized'
#     }
#     print(code)
#     response = requests.get(token_exchange_url, params=params)
#     data = response.json()
#
#     if 'access_token' in data:
#         access_token = data['access_token']
#         return access_token
#     else:
#         # Обработка ошибок
#         error_message = data.get('error', {}).get('message', 'Не удалось обменять код на токен.')
#         print(f"Ошибка: {error_message}")
#         return None
#
#
# app = Flask(__name__)
# from flask import Flask, request, jsonify
#
# app = Flask(__name__)
#
#
# @app.route('/authorize', methods=['GET'])
# def authorize():
#     data = request.json
#     auth_code = data.get('code')
#
#     # Выполните запрос к Facebook API для обмена кода на access token
#     # Используйте ваш client_id, client_secret и auth_code для этого запроса
#     # Здесь вы должны выполнить запрос к Facebook API с использованием библиотеки requests
#
#     # Пример:
#     response = requests.get('https://graph.facebook.com/v18.0/oauth/access_token', params={
#         'client_id': '323958937015510',
#         'client_secret': '4017320d9d5dcc49869874e73904b872',
#         'code': auth_code,
#         'redirect_uri': 'https://localhost:5000/'
#     })
#
#     # После успешного запроса, вы можете вернуть access_token клиенту
#     # Пример:
#     access_token = response.json().get('access_token')
#
#     # Вернем имитированный токен для примера
#     # access_token = 'fake_access_token'
#
#     return jsonify({'access_token': access_token})
#
# print(authorize)
# # @app.route('/login/authorized', methods=['GET'])
# # def authorized():
# #     auth_code = request.args.get('code')
# #     access_token = exchange_code_for_token('323958937015510', '4017320d9d5dcc49869874e73904b872', auth_code)
# #
# #     # Теперь у вас есть access_token, который вы можете использовать в вашем приложении
# #
# #     return access_token
# @app.route('/login/authorized', methods=['GET'])
# def authorized():
#     auth_code = request.args.get('code')
#     if auth_code:
#         access_token = exchange_code_for_token('323958937015510', '4017320d9d5dcc49869874e73904b872', auth_code)
#
#         if access_token:
#             return jsonify({'access_token': access_token})
#         else:
#             return jsonify({'error': 'Не удалось обменять код на токен.'}), 500
#     else:
#         return jsonify({'error': 'Не получен код авторизации.'}), 400
#
#
#
# if __name__ == '__main__':
#     app.run(debug=True, host='localhost', port=5000, ssl_context=(
#         'C:\\Users\Professional\\Downloads\\openssl-3.2.0\\openssl-3.2.0\\demos\\sslecho\\cert.pem',
#         'C:\\Users\Professional\\Downloads\\openssl-3.2.0\\openssl-3.2.0\\demos\\sslecho\\key.pem'))
#     webbrowser.open('https://localhost:5000/authorize')
# print(authorized())

