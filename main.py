# import csv
# with open("C:/Users/Professional/Downloads/asd.csv", 'r', encoding='utf-8') as file:
#     reader = csv.reader(file)
#     for row in reader:
#         for label in row:
#             print(label)
# Подключаем библиотеки
import httplib2
import googleapiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

CREDENTIALS_FILE = 'mypthon-401718-ae6b44a07d8c.json'  # Имя файла с закрытым ключом, вы должны подставить свое

# Читаем ключи из файла
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth'
                                                                                  '/spreadsheets',
                                                                                  'https://www.googleapis.com/auth'
                                                                                  '/drive'])

httpAuth = credentials.authorize(httplib2.Http()) # Авторизуемся в системе
service = googleapiclient.discovery.build('sheets', 'v4', http = httpAuth) # Выбираем работу с таблицами и 4 версию API

spreadsheet = service.spreadsheets().create(body = {
    'properties': {'title': 'Первый тестовый документ', 'locale': 'ru_RU'},
    'sheets': [{'properties': {'sheetType': 'GRID',
                               'sheetId': 0,
                               'title': 'Лист номер один',
                               'gridProperties': {'rowCount': 100, 'columnCount': 15}}}]
}).execute()
spreadsheetId = spreadsheet['spreadsheetId'] # сохраняем идентификатор файла
driveService = googleapiclient.discovery.build('drive', 'v3', http = httpAuth) # Выбираем работу с Google Drive и 3 версию API
access = driveService.permissions().create(
    fileId = spreadsheetId,
    body = {'type': 'user', 'role': 'writer', 'emailAddress': 'alnurt00@gmail.com'},  # Открываем доступ на редактирование
    fields = 'id'
).execute()
print('https://docs.google.com/spreadsheets/d/' + spreadsheetId)