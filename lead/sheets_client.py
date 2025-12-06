import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
load_dotenv(dotenv_path=".env")


class SheetsClient:
    def __init__(self):
        scope = ["https://www.googleapis.com/auth/spreadsheets"]
        creds_path = os.getenv("GOOGLE_CREDS_PATH")
        sheet_id = os.getenv("SHEET_ID")

        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
        client = gspread.authorize(creds)

        self.sheet = client.open_by_key(sheet_id).sheet1

    def get_all_leads(self):
        return self.sheet.get_all_records()

    def update_cell(self, row, col_name, value):
        header = self.sheet.row_values(1)
        col_index = header.index(col_name) + 1
        self.sheet.update_cell(row, col_index, value)

    def find_row_by_lead_id(self, lead_id):
        col_values = self.sheet.col_values(1)  # column A contains id
        if lead_id in col_values:
            return col_values.index(lead_id) + 1
        return None
