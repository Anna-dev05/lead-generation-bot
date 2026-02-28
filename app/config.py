import os
from dataclasses import dataclass
from dotenv import load_dotenv


@dataclass
class Config:
    bot_token: str
    admin_id: int
    google_creds_path: str
    sheet_id: str
    sheet_name: str


def load_config() -> Config:
    load_dotenv()

    token = os.getenv("BOT_TOKEN")
    admin_id = os.getenv("ADMIN_ID")
    creds_path = os.getenv("GOOGLE_CREDS_PATH")
    sheet_id = os.getenv("SHEET_ID")
    sheet_name = os.getenv("SHEET_NAME", "Sheet1")

    if not token:
        raise ValueError("BOT_TOKEN is missing. Put it into .env")
    if not admin_id:
        raise ValueError("ADMIN_ID is missing. Put it into .env")
    if not creds_path:
        raise ValueError("GOOGLE_CREDS_PATH is missing. Put it into .env")
    if not sheet_id:
        raise ValueError("SHEET_ID is missing. Put it into .env")

    return Config(
        bot_token=token,
        admin_id=int(admin_id),
        google_creds_path=creds_path,
        sheet_id=sheet_id,
        sheet_name=sheet_name,
    )
