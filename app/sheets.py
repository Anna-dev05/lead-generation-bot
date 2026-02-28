import os
import json
import gspread
from gspread.exceptions import WorksheetNotFound
from google.oauth2.service_account import Credentials

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

HEADERS = [
    "created_at",
    "name",
    "phone",
    "email",
    "telegram",
    "message",
    "user_id",
    "username",
]


def get_worksheet():
    # 1. Пытаемся достать текст ключа из переменной Railway
    google_creds_json = os.getenv("GOOGLE_CREDS_JSON")
    
    if google_creds_json:
        # СЛУЧАЙ ДЛЯ СЕРВЕРА: читаем данные прямо из памяти
        creds_info = json.loads(google_creds_json)
        creds = Credentials.from_service_account_info(creds_info, scopes=SCOPES)
    else:
        # СЛУЧАЙ ДЛЯ КОМПЬЮТЕРА: читаем из файла
        # Используем путь из твоего конфига
        creds = Credentials.from_service_account_file(config.google_creds_path, scopes=SCOPES)
        
    # Процесс авторизации
    client = gspread.authorize(creds)
    sheet = client.open_by_key(config.sheet_id)
    return sheet.get_worksheet(0)
    _ensure_headers(ws)
    return ws


def _ensure_headers(ws) -> None:
    """
    If the sheet is empty (no values) or first row is empty -> write headers.
    """
    values = ws.get_all_values()
    if not values:
        ws.append_row(HEADERS, value_input_option="USER_ENTERED")
        return

    first_row = values[0] if values else []
    if not any(cell.strip() for cell in first_row):
        ws.update("A1", [HEADERS])


def append_lead_row(
    worksheet,
    created_at: str,
    name: str,
    phone: str,
    email: str,
    telegram: str,
    message: str,
    user_id: int,
    username: str | None,
):
    """
    Append one lead row to the worksheet.

    Expected columns:
    created_at | name | phone | email | telegram | message | user_id | username
    """
    worksheet.append_row(
        [
            created_at,
            name,
            phone,
            email or "",
            telegram or "",
            message or "",
            str(user_id),
            username or "",
        ],
        value_input_option="USER_ENTERED",
    )
