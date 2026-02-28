import sys
import os
import asyncio
import logging

# ПРИНУДИТЕЛЬНО ДОБАВЛЯЕМ ПУТЬ К ПАПКЕ С КОДОМ
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Теперь импортируем без приставки "app.", так как мы уже "внутри" или рядом
try:
    from app.config import load_config
    from app.handlers import router
    from app.sheets import get_worksheet
    from app.database import init_db
except ModuleNotFoundError:
    # Если первый вариант не сработал, пробуем прямой импорт
    from config import load_config
    from handlers import router
    from sheets import get_worksheet
    from database import init_db

async def main():
    logging.basicConfig(level=logging.INFO)

    config = load_config()

    bot = Bot(token=config.bot_token)
    dp = Dispatcher()

    dp.workflow_data["admin_id"] = config.admin_id

    worksheet = get_worksheet() 
    
    dp.workflow_data["worksheet"] = worksheet

    init_db()

    dp.include_router(router)

    await dp.start_polling(bot)


