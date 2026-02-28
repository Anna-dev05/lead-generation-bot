import asyncio
import logging
import sys
import os

# --- ИСПРАВЛЕНИЕ ПУТЕЙ ИМПОРТА ---
# Это заставляет Python видеть папку app и файлы внутри неё
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

app_path = os.path.join(current_dir, 'app')
if app_path not in sys.path:
    sys.path.append(app_path)

from aiogram import Bot, Dispatcher

# Умный импорт: пробует найти файлы внутри app
try:
    from app.config import load_config
    from app.handlers import router
    from app.sheets import get_worksheet
    from app.database import init_db
except (ImportError, ModuleNotFoundError):
    from config import load_config
    from handlers import router
    from sheets import get_worksheet
    from database import init_db

async def main():
    # Настройка логов для Railway (чтобы они отображались в панели)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        stream=sys.stdout
    )
    
    logging.info("🚀 ЗАПУСК БОТА...")

    try:
        # Загружаем конфиг
        config = load_config()
        bot = Bot(token=config.bot_token)
        dp = Dispatcher()

        # Подключаем Google Таблицы
        logging.info("📊 Подключение к Google Sheets...")
        worksheet = get_worksheet()
        
        # Передаем данные в хендлеры
        dp.workflow_data["admin_id"] = config.admin_id
        dp.workflow_data["worksheet"] = worksheet

        # Инициализируем базу данных (теперь файл database.py должен быть создан!)
        logging.info("💾 Инициализация базы данных...")
        init_db()
        
        # Подключаем хендлеры
        dp.include_router(router)

        logging.info("✅ БОТ УСПЕШНО ЗАПУЩЕН!")
        
        # Запуск опроса Telegram
        await dp.start_polling(bot)
        
    except Exception as e:
        logging.error(f"❌ КРИТИЧЕСКАЯ ОШИБКА: {e}", exc_info=True)

if __name__ == "__main__":
    asyncio.run(main())





