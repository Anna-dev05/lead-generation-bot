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


def get_worksheet(sheet_id: str, creds_path: str, sheet_name: str):
    """
    Connect to Google Sheets and return worksheet by name.
    If worksheet doesn't exist -> create it.
    If worksheet is empty -> add headers.
    """
    creds = Credentials.from_service_account_file(creds_path, scopes=SCOPES)
    client = gspread.authorize(creds)

    spreadsheet = client.open_by_key(sheet_id)

    try:
        ws = spreadsheet.worksheet(sheet_name)
    except WorksheetNotFound:
        # Create a new worksheet (rows/cols can be adjusted)
        ws = spreadsheet.add_worksheet(title=sheet_name, rows=2000, cols=len(HEADERS))

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
