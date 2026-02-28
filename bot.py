import asyncio
import logging

from aiogram import Bot, Dispatcher

from app.config import load_config
from app.handlers import router
from app.sheets import get_worksheet
from app.storage import init_db  


async def main():
    logging.basicConfig(level=logging.INFO)

    config = load_config()

    bot = Bot(token=config.bot_token)
    dp = Dispatcher()

    dp.workflow_data["admin_id"] = config.admin_id

    worksheet = get_worksheet(
        sheet_id=config.sheet_id,
        creds_path=config.google_creds_path,   # <-- важно
        sheet_name=config.sheet_name
    )
    dp.workflow_data["worksheet"] = worksheet

    init_db()

    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

