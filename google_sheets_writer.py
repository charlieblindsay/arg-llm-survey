from google.oauth2 import service_account
from googleapiclient.discovery import build


class GoogleSheetsWriter:
    def __init__(self, spreadsheet_id, sheet_name):
        self.credentials_path = 'google_sheets_auth.json'

        scopes = ['https://www.googleapis.com/auth/spreadsheets']
        credentials = service_account.Credentials.from_service_account_file(
            self.credentials_path, scopes=scopes
        )

        self.service = build('sheets', 'v4', credentials=credentials)
        self.sheet_name = sheet_name
        self.spreadsheet_id = spreadsheet_id

    def write_to_sheets(self, new_line_data):
        sheet_range = f"{self.sheet_name}!A:A"

        values = [new_line_data]

        body = {
            'values': values
        }

        self.service.spreadsheets().values().append(
            spreadsheetId=self.spreadsheet_id,
            range=sheet_range,
            valueInputOption='RAW',
            body=body
        ).execute()
