from google.oauth2 import service_account
from googleapiclient.discovery import build

class GoogleSheet:
    SPREADSHEET_ID = '1Q_FhA_Og0_5aZLQHNLq1JJnpcsIgqvgDW1mWa0q6kXY'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    service = None

    def __init__(self):
        self.token = self._get_token()
        self.service = self._init_service()

    def _get_token(self):
        credentials = service_account.Credentials.from_service_account_file(
            'mypthon-401718-ae6b44a07d8c.json',
            scopes=self.SCOPES
        )
        return credentials

    def _init_service(self):
        return build('sheets', 'v4', credentials=self.token)

    def append_values(self, range, values):
        body = {
            'values': values,
        }
        result = self.service.spreadsheets().values().append(
            spreadsheetId=self.SPREADSHEET_ID,
            range=range,
            valueInputOption='USER_ENTERED',
            body=body
        ).execute()
        print('{0} cells appended.'.format(result.get('updates').get('updatedCells')))
