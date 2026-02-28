import os
import json
import gspread
from google.oauth2.service_account import Credentials
from app import config

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def get_worksheet():
    google_creds_json = os.getenv("GOOGLE_CREDS_JSON")
    # Берем SHEET_ID напрямую из переменных Railway
    sheet_id = os.getenv("SHEET_ID") 
    
    if google_creds_json:
        creds_info = json.loads(google_creds_json)
        creds = Credentials.from_service_account_info(creds_info, scopes=SCOPES)
    else:
        creds = Credentials.from_service_account_file(config.google_creds_path, scopes=SCOPES)
        
    client = gspread.authorize(creds)
    # Используем переменную sheet_id напрямую
    sheet = client.open_by_key(sheet_id) 
    return sheet.get_worksheet(0)

def append_lead_row(worksheet, created_at, name, phone, email, telegram, message, user_id, username):
    worksheet.append_row(
        [created_at, name, phone, email or "", telegram or "", message or "", str(user_id), username or ""],
        value_input_option="USER_ENTERED",

    )
