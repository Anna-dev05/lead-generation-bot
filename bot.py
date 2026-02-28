import sys
import os
import asyncio
import logging

# Добавляем путь к папке app в систему поиска Python
current_dir = os.path.dirname(os.path.abspath(__file__))
app_path = os.path.join(current_dir, 'app')
if app_path not in sys.path:
    sys.path.append(app_path)

from aiogram import Bot, Dispatcher

# ТЕПЕРЬ ИМПОРТИРУЕМ НАПРЯМУЮ:
try:
    from config import load_config
    from handlers import router
    from sheets import get_worksheet
    from database import init_db
except ImportError:
    # Запасной вариант для локального запуска
    from app.config import load_config
    from app.handlers import router
    from app.sheets import get_worksheet
    from app.database import init_db
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




