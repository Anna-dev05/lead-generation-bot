import re
import logging
from aiogram import Router, types, Bot, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from states import LeadForm
from keyboards import main_menu, phone_keyboard, confirm_keyboard
from storage import save_lead
from sheets import append_lead_row

# Инициализируем логгер для этого файла
logger = logging.getLogger(__name__)

router = Router()

# === НАСТРОЙКИ И КОНСТАНТЫ (Senior approach) ===
HOTEL_NAME = "Bristol"
EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")

MIN_NAME_LEN = 2
MIN_PHONE_LEN = 6
MIN_MSG_LEN = 3

# --- КЛАВИАТУРА ПРОПУСКА ---
def skip_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="⏭ Skip")]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def _welcome_text() -> str:
    return (
        f"Hello! 👋 Welcome to *{HOTEL_NAME}*.\n\n"
        "We’re sorry we couldn’t respond right now.\n"
        "Please leave your phone number and a short message — "
        "our administrator will call you back as soon as possible.\n\n"
        "Tap **📩 Leave a message** to continue."
    )

def _about_text() -> str:
    return (
        f"ℹ️ *About {HOTEL_NAME} Assistant*\n\n"
        "This assistant helps when we miss your call.\n"
        "Phone number is required. Email and Telegram are optional.\n\n"
        "We will contact you as soon as possible."
    )

def _preview(data: dict) -> str:
    email = data.get("email") or "-"
    tg = data.get("telegram") or "-"
    msg = data.get("message") or "-"
    return (
        "✅ *Please confirm your details*\n\n"
        f"👤 *Name:* {data.get('name')}\n"
        f"📞 *Phone:* {data.get('phone')}\n"
        f"📧 *Email:* {email}\n"
        f"💬 *Telegram:* {tg}\n"
        f"📝 *Message:* {msg}\n\n"
        "Tap **Send** to submit. We will get back to you as soon as possible."
    )

@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext) -> None:
    logger.info(f"User {message.from_user.id} started the bot.")
    await state.clear()
    await message.answer(_welcome_text(), parse_mode="Markdown", reply_markup=main_menu())

@router.message(F.text == "ℹ️ About")
async def about(message: types.Message) -> None:
    await message.answer(_about_text(), parse_mode="Markdown", reply_markup=main_menu())

@router.message(F.text == "❌ Cancel")
async def cancel(message: types.Message, state: FSMContext) -> None:
    logger.info(f"User {message.from_user.id} cancelled the action.")
    await state.clear()
    await message.answer("Cancelled ✅", reply_markup=main_menu())

@router.message(F.text == "📩 Leave a message")
async def start_form(message: types.Message, state: FSMContext) -> None:
    logger.info(f"User {message.from_user.id} started the lead form.")
    await state.clear()
    await message.answer("Great — what is your name?", reply_markup=ReplyKeyboardRemove())
    await state.set_state(LeadForm.name)

@router.message(LeadForm.name)
async def step_name(message: types.Message, state: FSMContext) -> None:
    name = message.text.strip()
    if len(name) < MIN_NAME_LEN:
        await message.answer(f"Please enter a valid name (at least {MIN_NAME_LEN} characters):")
        return

    await state.update_data(name=name)
    await message.answer(
        "Please share your phone number (tap the button) or type it manually:",
        reply_markup=phone_keyboard()
    )
    await state.set_state(LeadForm.phone)

@router.message(LeadForm.phone, F.contact)
async def step_phone_contact(message: types.Message, state: FSMContext) -> None:
    phone = (message.contact.phone_number or "").strip()
    if len(phone) < MIN_PHONE_LEN:
        await message.answer("That phone number looks too short. Please type it manually:")
        return

    await state.update_data(phone=phone)
    await _ask_email(message, state)

@router.message(LeadForm.phone, F.text)
async def step_phone_text(message: types.Message, state: FSMContext) -> None:
    phone = message.text.strip()
    if len(phone) < MIN_PHONE_LEN:
        await message.answer("That phone number looks too short. Please enter it again:")
        return

    await state.update_data(phone=phone)
    await _ask_email(message, state)

async def _ask_email(message: types.Message, state: FSMContext) -> None:
    await state.set_state(LeadForm.email)
    await message.answer(
        "Please enter your email address (or tap Skip):",
        reply_markup=skip_keyboard()
    )

@router.message(LeadForm.email)
async def step_email(message: types.Message, state: FSMContext) -> None:
    email = message.text.strip()
    
    if email == "⏭ Skip":
        logger.info(f"User {message.from_user.id} skipped email.")
        await state.update_data(email="")
        await _ask_telegram(message, state)
        return

    if not EMAIL_RE.match(email):
        await message.answer("Please enter a valid email (example: name@email.com) or tap Skip:", reply_markup=skip_keyboard())
        return

    await state.update_data(email=email)
    await _ask_telegram(message, state)

async def _ask_telegram(message: types.Message, state: FSMContext) -> None:
    await state.set_state(LeadForm.telegram)
    await message.answer(
        "Please enter your Telegram username (or tap Skip):",
        reply_markup=skip_keyboard()
    )

@router.message(LeadForm.telegram)
async def step_telegram(message: types.Message, state: FSMContext) -> None:
    text = message.text.strip()
    
    if text == "⏭ Skip":
        logger.info(f"User {message.from_user.id} skipped telegram.")
        await state.update_data(telegram="")
        await _ask_message(message, state)
        return

    telegram = text if text.startswith("@") else f"@{text}"
    if len(telegram) < 3:
        await message.answer("Telegram username looks invalid. Please enter again or tap Skip:", reply_markup=skip_keyboard())
        return

    await state.update_data(telegram=telegram)
    await _ask_message(message, state)

async def _ask_message(message: types.Message, state: FSMContext) -> None:
    await state.set_state(LeadForm.message)
    await message.answer(
        "Please leave a short message.\n"
        "For example: *“Please call me tomorrow after 6 PM”* or *“Late check-in at 22:00”*.\n\n"
        "(Or tap Skip if you just want us to call back)",
        parse_mode="Markdown",
        reply_markup=skip_keyboard()
    )

@router.message(LeadForm.message)
async def step_message(message: types.Message, state: FSMContext) -> None:
    msg = message.text.strip()
    
    if msg == "⏭ Skip":
        logger.info(f"User {message.from_user.id} skipped message.")
        msg = "No message provided"
    elif len(msg) < MIN_MSG_LEN:
        await message.answer(f"Please enter a short message (at least {MIN_MSG_LEN} characters) or tap Skip:", reply_markup=skip_keyboard())
        return

    await state.update_data(message=msg)

    data = await state.get_data()
    await state.set_state(LeadForm.confirm)

    await message.answer(
        _preview(data),
        parse_mode="Markdown",
        reply_markup=confirm_keyboard()
    )

@router.callback_query(F.data == "lead_edit")
async def lead_edit(callback: types.CallbackQuery, state: FSMContext) -> None:
    logger.info(f"User {callback.from_user.id} decided to edit the lead.")
    await callback.answer()
    await state.set_state(LeadForm.name)
    await callback.message.answer("No problem. Please enter your name again:", reply_markup=ReplyKeyboardRemove())

@router.callback_query(F.data == "lead_confirm")
async def lead_confirm(
    callback: types.CallbackQuery,
    state: FSMContext,
    bot: Bot,
    admin_id: int,
    worksheet,
) -> None:
    await callback.answer()

    data = await state.get_data()
    name = data.get("name")
    phone = data.get("phone")
    email = data.get("email") or ""
    telegram = data.get("telegram") or ""
    message_text = data.get("message") or ""

    if not name or not phone:
        logger.warning(f"User {callback.from_user.id} reached confirm without name or phone.")
        await state.clear()
        await callback.message.answer("Something went wrong. Please start again: /start", reply_markup=main_menu())
        return

    # Отправляем статус "печатает...", пока идет сохранение в базы
    await bot.send_chat_action(chat_id=callback.message.chat.id, action="typing")

    # SQLite save
    try:
        created_at = save_lead(
            name=name,
            phone=phone,
            email=email,
            telegram=telegram,
            message=message_text,
            user_id=callback.from_user.id,
            username=callback.from_user.username
        )
        logger.info(f"Lead from {callback.from_user.id} saved to DB.")
    except Exception as e:
        logger.error(f"DB Error: {e}")
        created_at = "Unknown"

    # Google Sheets
    try:
        append_lead_row(
            worksheet=worksheet,
            created_at=created_at,
            name=name,
            phone=phone,
            email=email,
            telegram=telegram,
            message=message_text,
            user_id=callback.from_user.id,
            username=callback.from_user.username,
        )
        logger.info(f"Lead from {callback.from_user.id} saved to Google Sheets.")
    except Exception as e:
        logger.error(f"Google Sheets Error: {e}")
        await bot.send_message(admin_id, f"⚠️ Could not write to Google Sheets: {e}")

    # Admin notify
    admin_text = (
        f"🆕 New message ({HOTEL_NAME})\n"
        f"⏱ Time: {created_at}\n"
        f"👤 Name: {name}\n"
        f"📞 Phone: {phone}\n"
        f"📧 Email: {email or '-'}\n"
        f"💬 Telegram: {telegram or '-'}\n"
        f"📝 Message: {message_text or '-'}\n"
        f"🆔 User ID: {callback.from_user.id}\n"
    )

    if callback.from_user.username:
        admin_text += f"🔗 Username: @{callback.from_user.username}\n"
    else:
        admin_text += "🔗 Username: (no username)\n"

    await bot.send_message(admin_id, admin_text)

    await callback.message.answer(
        "✅ Thank you! Your message has been sent.\n"
        "Our administrator will contact you as soon as possible.",
        reply_markup=main_menu()
    )
    await state.clear()




