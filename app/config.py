import os
from dataclasses import dataclass
from dotenv import load_dotenv

@dataclass
class Config:
    bot_token: str
    admin_id: int
    google_creds_path: str | None  # Сделали необязательным
    sheet_id: str
    sheet_name: str

def load_config() -> Config:
    load_dotenv()

    token = os.getenv("BOT_TOKEN")
    admin_id = os.getenv("ADMIN_ID")
    sheet_id = os.getenv("SHEET_ID")
    sheet_name = os.getenv("SHEET_NAME", "Sheet1")
    
    # Пытаемся взять путь к файлу, если он есть
    creds_path = os.getenv("GOOGLE_CREDS_PATH")
    
    # Проверяем только самые важные вещи
    if not token:
        raise ValueError("BOT_TOKEN is missing в переменных Railway!")
    if not admin_id:
        raise ValueError("ADMIN_ID is missing в переменных Railway!")
    if not sheet_id:
        raise ValueError("SHEET_ID is missing в переменных Railway!")

    # Если мы НЕ на сервере (нет GOOGLE_CREDS_JSON), то нам ОБЯЗАТЕЛЬНО нужен путь к файлу
    if not os.getenv("GOOGLE_CREDS_JSON") and not creds_path:
         raise ValueError("На компьютере должен быть GOOGLE_CREDS_PATH или файл credentials.json")

    return Config(
        bot_token=token,
        admin_id=int(admin_id),
        google_creds_path=creds_path,
        sheet_id=sheet_id,
        sheet_name=sheet_name,
    )