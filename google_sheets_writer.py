from google.oauth2 import service_account
from googleapiclient.discovery import build
import streamlit as st


def get_credentials():
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    try:
        # Try loading a local file first
        creds = service_account.Credentials.from_service_account_file(
            "google_sheets_auth.json",
            scopes=scopes
        )
    except (FileNotFoundError, OSError):
        # Fall back to streamlit secrets
        svcacct_info = st.secrets["gcp_service_account"]
        creds = service_account.Credentials.from_service_account_info(
            svcacct_info,
            scopes=scopes
        )
    return creds


class GoogleSheetsWriter:
    def __init__(self, spreadsheet_id):
        self.credentials_path = 'google_sheets_auth.json'

        credentials = get_credentials()

        self.service = build('sheets', 'v4', credentials=credentials)
        self.spreadsheet_id = spreadsheet_id

    def write_to_sheets(self, new_line_data, sheet_name):
        sheet_range = f"{sheet_name}!A:A"

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
