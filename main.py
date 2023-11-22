import sys
import webbrowser

import facebook
import facebook_business.bootstrap
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from Naked.toolshed.shell import execute_js, muterun_js
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adsinsights import AdsInsights
from facebook_business.adobjects.campaign import Campaign
import telebot;
from facebook_business.adobjects.adaccountuser import AdAccountUser as AdUser
from pandas import DataFrame
import os.path
import os.path
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
class GoogleSheet:
  SPREADSHEET_ID = '1Q_FhA_Og0_5aZLQHNLq1JJnpcsIgqvgDW1mWa0q6kXY'
  SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
  service = None

  def __init__(self):
    creds = None
    if os.path.exists('token.pickle'):
      with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)

    if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
      else:
        print('flow')
        flow = InstalledAppFlow.from_client_secrets_file(
          'credentials.json', self.SCOPES)
        creds = flow.run_local_server(port=0)
      with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

    self.service = build('sheets', 'v4', credentials=creds)

  def updateRangeValues(self, range, values):
    data = [{
      'range': range,
      'values': values
    }]
    body = {
      'valueInputOption': 'USER_ENTERED',
      'data': data
    }
    result = self.service.spreadsheets().values().batchUpdate(spreadsheetId=self.SPREADSHEET_ID, body=body).execute()
    print('{0} cells updated.'.format(result.get('totalUpdatedCells')))

def auth():
    file_name = 'index.html'

    request_file_content = open(open(file_name).read(), 'rb')
    return request_file_content

def main(df):

  gs = GoogleSheet()
  fs = auth()
  print(fs)
  test_range = 'test!A:G'
  df_json = df.values.tolist()
  test_values = df_json
  gs.updateRangeValues(test_range, test_values)

my_access_token = 'EAAEmo5Fc1NYBOzZCbfBnqJFoYmGqJqpE1T469qTP4yo9JdH3Cyt60JVWZACvQXiA6qu0wIY4ILgFAQP83kLJvpLMoUYMQma0vFuDci6Vknk6JNHY01Ae458HIVAA3eWXNduARbZAZBsSMdUZBp7qhLs7SescIqaChUSCZAhbxuBMvLdPNg84ghQAvj3aOwvwCgy4KB'
my_app_id = '323958937015510'
my_app_secret = '4017320d9d5dcc49869874e73904b872'
FacebookAdsApi.init(my_app_id, my_app_secret, my_access_token)
me = AdUser(fbid='me')
my_accounts = list(me.get_ad_accounts(fields=[AdAccount.Field.name]))
my_account = my_accounts[0]
CampaignName = my_account.get_campaigns(fields=[
    Campaign.Field.name,
])
fields = [
    AdsInsights.Field.adset_name,
    AdsInsights.Field.ad_name,
    AdsInsights.Field.spend,
    AdsInsights.Field.impressions,
    AdsInsights.Field.date_start,
    AdsInsights.Field.date_stop,
    AdsInsights.Field.campaign_name,
    AdsInsights.Field.dda_results,
    AdsInsights.Field.cpm,
    AdsInsights.Field.impressions]
mas = []
for i in CampaignName:
    campdata = i.get_insights(params=
                              {'level': 'adset',
                               'date_preset': 'this_month',
                               'time_increment': 1},
                              fields=fields)
    mas.append(campdata)
camp_name_data = []
camp_name_spend = []
camp_date_start = []
camp_date_stop = []
camp_compaign = []
# camp_result = []
camp_cpm = []
camp_impressions = []
for f in mas:
    for j in f:
        camp_name_data.append(j['adset_name'])
        camp_name_spend.append(j['spend'])
        camp_date_start.append(j['date_start'])
        camp_date_stop.append(j['date_stop'])
        camp_compaign.append(j['campaign_name'])
        # camp_result.append(j['dda_results'])
        camp_cpm.append(j['cpm'])
        camp_impressions.append(j['impressions'])
df = DataFrame()
df['Date_start'] = camp_date_start
df['Date_stop'] = camp_date_stop
df['Spend'] = camp_name_spend
df['Name'] = camp_name_data
df['Compaign'] = camp_compaign
# df['Result'] = camp_result
df['CPM'] = camp_cpm
df['Impressions'] = camp_impressions

print(df)
bot = telebot.TeleBot('6713056294:AAFAr-2ipWydHjlsiXgKPuxGI-YmeGStvOQ');

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/start":
        main(df)

bot.polling(none_stop=True, interval=0)





# CREDENTIALS_FILE = 'mypthon-401718-ae6b44a07d8c.json'  # Имя файла с закрытым ключом, вы должны подставить свое
# credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth'
#                                                                                   '/spreadsheets',
#                                                                                   'https://www.googleapis.com/auth'
#                                                                                   '/drive'])
# httpAuth = credentials.authorize(httplib2.Http()) # Авторизуемся в системе
# service = googleapiclient.discovery.build('sheets', 'v4', http = httpAuth) # Выбираем работу с таблицами и 4 версию API
# spreadsheet = service.spreadsheets().create(body = {
#     'properties': {'title': 'Первый тестовый документ', 'locale': 'ru_RU'},
#     'sheets': [{'properties': {'sheetType': 'GRID',
#                                'sheetId': 0,
#                                'title': 'Лист номер один',
#                                'gridProperties': {'rowCount': 100, 'columnCount': 15}}}]
# }).execute()
# spreadsheetId = spreadsheet['spreadsheetId'] # сохраняем идентификатор файла
# driveService = googleapiclient.discovery.build('drive', 'v3', http = httpAuth) # Выбираем работу с Google Drive и 3 версию API
# access = driveService.permissions().create(
#     fileId = spreadsheetId,
#     body = {'type': 'user', 'role': 'writer', 'emailAddress': 'alnurt00@gmail.com'},  # Открываем доступ на редактирование
#     fields = 'id'
# ).execute()
# results = service.spreadsheets().batchUpdate(
#     spreadsheetId=spreadsheetId,
#     body=
#     {
#         "requests": [
#             {
#                 "addSheet": {
#                     "properties": {
#                         "title": "Еще один лист",
#                         "gridProperties": {
#                             "rowCount": 20,
#                             "columnCount": 12
#                         }
#                     }
#                 }
#             }
#         ]
#     }).execute()
# spreadsheet = service.spreadsheets().get(spreadsheetId=spreadsheetId).execute()
# sheetList = spreadsheet.get('sheets')
# for sheet in sheetList:
#     print(sheet['properties']['sheetId'], sheet['properties']['title'])
#
# sheetId = sheetList[0]['properties']['sheetId']
#
# for row in df:
#         for label in row:
#             {"range":
#                 {
#                     "sheetId": sheetId,  # ID листа
#                     "startRowIndex": 1,  # Со строки номер startRowIndex
#                     "endRowIndex": len(label),  # по endRowIndex - 1 (endRowIndex не входит!)
#                     "startColumnIndex": 0,  # Со столбца номер startColumnIndex
#                     "endColumnIndex": len(row)  # по endColumnIndex - 1
#                 }}
#             results = service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheetId, body = {
#                 "valueInputOption": "USER_ENTERED", # Данные воспринимаются, как вводимые пользователем (считается значение формул)
#                 "data": [
#                     {"range": "Лист номер один!B2:D5",
#                      "majorDimension": "ROWS",     # Сначала заполнять строки, затем столбцы
#                      "values": [
#                                 label  # Заполняем вторую строку
#                                ]}
#                 ]
#             }).execute()
# print('https://docs.google.com/spreadsheets/d/' + spreadsheetId)

# from facebook_business.objects import AdCampaign
# campaign = AdCampaign('AD_CAMPAIGN_ID')
# params = {
#     'date_preset': AdCampaign.Preset.last_7_days,
# }
# insights = campaign.get_insights(params=params)
# print(insights)
# import csv
#
# # Подключаем библиотеки
# import requests
# from bs4 import BeautifulSoup as bs
# import pandas as pd
# import httplib2
# import googleapiclient.discovery
# from oauth2client.service_account import ServiceAccountCredentials
#
# # labels = []
# # i = 0
# #
# # CREDENTIALS_FILE = 'mypthon-401718-ae6b44a07d8c.json'  # Имя файла с закрытым ключом, вы должны подставить свое
# #
# # # Читаем ключи из файла
# credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth'
#                                                                                   '/spreadsheets',
#                                                                                   'https://www.googleapis.com/auth'
#                                                                                   '/drive'])
# #
# # httpAuth = credentials.authorize(httplib2.Http()) # Авторизуемся в системе
# # service = googleapiclient.discovery.build('sheets', 'v4', http = httpAuth) # Выбираем работу с таблицами и 4 версию API
# #
# spreadsheet = service.spreadsheets().create(body = {
#     'properties': {'title': 'Первый тестовый документ', 'locale': 'ru_RU'},
#     'sheets': [{'properties': {'sheetType': 'GRID',
#                                'sheetId': 0,
#                                'title': 'Лист номер один',
#                                'gridProperties': {'rowCount': 100, 'columnCount': 15}}}]
# }).execute()
# # spreadsheetId = spreadsheet['spreadsheetId'] # сохраняем идентификатор файла
# # driveService = googleapiclient.discovery.build('drive', 'v3', http = httpAuth) # Выбираем работу с Google Drive и 3 версию API
# # access = driveService.permissions().create(
# #     fileId = spreadsheetId,
# #     body = {'type': 'user', 'role': 'writer', 'emailAddress': 'alnurt00@gmail.com'},  # Открываем доступ на редактирование
# #     fields = 'id'
# # ).execute()
# # results = service.spreadsheets().batchUpdate(
# #     spreadsheetId=spreadsheetId,
# #     body=
# #     {
# #         "requests": [
# #             {
# #                 "addSheet": {
# #                     "properties": {
# #                         "title": "Еще один лист",
# #                         "gridProperties": {
# #                             "rowCount": 20,
# #                             "columnCount": 12
# #                         }
# #                     }
# #                 }
# #             }
# #         ]
# #     }).execute()
# # # Получаем список листов, их Id и название
# # spreadsheet = service.spreadsheets().get(spreadsheetId=spreadsheetId).execute()
# # sheetList = spreadsheet.get('sheets')
# # for sheet in sheetList:
# #     print(sheet['properties']['sheetId'], sheet['properties']['title'])
# #
# # sheetId = sheetList[0]['properties']['sheetId']
# #
# #
# # with open("C:/Users/Professional/Downloads/asd.csv", 'r', encoding='utf-8') as file:
# #     reader = csv.reader(file)
# #     for row in reader:
# #         for label in row:
# #             {"range":
# #                 {
# #                     "sheetId": sheetId,  # ID листа
# #                     "startRowIndex": 1,  # Со строки номер startRowIndex
# #                     "endRowIndex": len(label),  # по endRowIndex - 1 (endRowIndex не входит!)
# #                     "startColumnIndex": 0,  # Со столбца номер startColumnIndex
# #                     "endColumnIndex": len(row)  # по endColumnIndex - 1
# #                 }}
# #             results = service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheetId, body = {
# #                 "valueInputOption": "USER_ENTERED", # Данные воспринимаются, как вводимые пользователем (считается значение формул)
# #                 "data": [
# #                     {"range": "Лист номер один!B2:D5",
# #                      "majorDimension": "ROWS",     # Сначала заполнять строки, затем столбцы
# #                      "values": [
# #                                 [label]  # Заполняем вторую строку
# #                                ]}
# #                 ]
# #             }).execute()
# # print('https://docs.google.com/spreadsheets/d/' + spreadsheetId)
#
#
#
#
# def parse():
#     URL_TEMPLATE = "https://www.facebook.com/adsviewreport/?saved_report_id=120200463156180052&client_creation_value=f8d893fc1b0328"
#     r = requests.get(URL_TEMPLATE)
#     print(r)
#
# print(parse())
