import sys
import os
import asyncio
import logging

sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from aiogram import Bot, Dispatcher
from config import load_config
from handlers import router
from sheets import get_worksheet
from database import init_db


async def main():
    # Настройка логов для Railway
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        stream=sys.stdout
    )
    logger = logging.getLogger(__name__)
    logger.info("🚀 Попытка запуска бота...")

    try:
        config = load_config()
        bot = Bot(token=config.bot_token)
        dp = Dispatcher()

        logger.info("📊 Подключение к Google Sheets...")
        worksheet = get_worksheet()
        
        dp.workflow_data["admin_id"] = config.admin_id
        dp.workflow_data["worksheet"] = worksheet

        logger.info("💾 Инициализация БД...")
        init_db()
        
        dp.include_router(router)

        logger.info("✅ Бот успешно запущен!")
        await dp.start_polling(bot)
        
    except Exception as e:
        logger.error(f"❌ Ошибка при запуске: {e}", exc_info=True)

if __name__ == "__main__":

    asyncio.run(main())
