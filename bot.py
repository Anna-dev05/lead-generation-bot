import sys
import os
import asyncio
import logging

# 1. Добавляем путь к папке app в системные пути поиска Python
current_dir = os.path.dirname(os.path.abspath(__file__))
app_path = os.path.join(current_dir, 'app')
sys.path.append(app_path)

# 2. Теперь импортируем модули напрямую (без приставки app.)
# Так как мы добавили путь к app в sys.path, Python найдет их там
try:
    from config import load_config
    from handlers import router
    from sheets import get_worksheet
    from database import init_db
    logging.info("Импорты успешно загружены напрямую из папки app")
except ImportError as e:
    logging.error(f"Ошибка импорта даже после настройки путей: {e}")
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



