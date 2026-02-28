import os
import json
import gspread
from gspread.exceptions import WorksheetNotFound
from google.oauth2.service_account import Credentials
from app import config  # ИСПРАВЛЕНО: Добавили импорт конфига

# ИСПРАВЛЕНО: Добавили Drive в SCOPES
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

HEADERS = [
    "created_at", "name", "phone", "email", 
    "telegram", "message", "user_id", "username",
]

def get_worksheet():
    google_creds_json = os.getenv("GOOGLE_CREDS_JSON")
    
    if google_creds_json:
        creds_info = json.loads(google_creds_json)
        creds = Credentials.from_service_account_info(creds_info, scopes=SCOPES)
    else:
        # Для работы на компьютере
        creds = Credentials.from_service_account_file(config.google_creds_path, scopes=SCOPES)
        
    client = gspread.authorize(creds)
    
    # ИСПРАВЛЕНО: Используем config.sheet_id правильно
    sheet = client.open_by_key(config.sheet_id)
    ws = sheet.get_worksheet(0)
    
    # Сначала проверяем заголовки, потом возвращаем лист
    _ensure_headers(ws)
    return ws

def _ensure_headers(ws) -> None:
    values = ws.get_all_values()
    if not values or not any(values[0]):
        ws.update("A1", [HEADERS])

def append_lead_row(worksheet, created_at, name, phone, email, telegram, message, user_id, username):
    worksheet.append_row(
        [created_at, name, phone, email or "", telegram or "", message or "", str(user_id), username or ""],
        value_input_option="USER_ENTERED",
    )
