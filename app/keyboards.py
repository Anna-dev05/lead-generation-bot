from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


def main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📩 Leave a message")],
            [KeyboardButton(text="ℹ️ About"), KeyboardButton(text="❌ Cancel")],
        ],
        resize_keyboard=True,
    )


def phone_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📞 Share phone number", request_contact=True)],
            [KeyboardButton(text="❌ Cancel")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def yes_no_keyboard(prefix: str) -> InlineKeyboardMarkup:
    # prefix: "email" or "tg"
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Yes", callback_data=f"{prefix}:yes"),
                InlineKeyboardButton(text="❌ No", callback_data=f"{prefix}:no"),
            ]
        ]
    )


def confirm_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Send", callback_data="lead_confirm"),
                InlineKeyboardButton(text="✏️ Edit", callback_data="lead_edit"),
            ]
        ]
    )
