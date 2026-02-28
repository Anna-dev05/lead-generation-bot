import asyncio
import logging
import sys
import os

# --- БЛОК ИСПРАВЛЕНИЯ ПУТЕЙ (Критически важно для Railway) ---
# Определяем путь к текущей папке и папке 'app'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.join(BASE_DIR, 'app')

# Добавляем их в поиск, чтобы Python видел файлы внутри 'app' без ошибок
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)
if APP_DIR not in sys.path:
    sys.path.append(APP_DIR)

from aiogram import Bot, Dispatcher

# Пытаемся импортировать модули. Если не находит через app., пробует напрямую.
try:
    from app.config import load_config
    from app.handlers import router
    from app.sheets import get_worksheet
    from app.database import init_db
except ImportError:
    from config import load_config
    from handlers import router
    from sheets import get_worksheet
    from database import init_db

async def main():
    # Настройка логирования, чтобы ты видела всё в панели Railway
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        stream=sys.stdout
    )
    logger = logging.getLogger(__name__)
    logger.info("🚀 ЗАПУСК БОТА...")

    try:
        # 1. Загрузка конфигурации
        config = load_config()
        bot = Bot(token=config.bot_token)
        dp = Dispatcher()

        # 2. Подключение к Google Таблице
        logger.info("📊 Подключаемся к Google Sheets...")
        worksheet = get_worksheet()
        
        # Передаем данные в хендлеры через workflow_data
        dp.workflow_data["admin_id"] = config.admin_id
        dp.workflow_data["worksheet"] = worksheet

        # 3. Инициализация базы данных SQLite
        logger.info("💾 Инициализация базы данных...")
        init_db()
        
        # 4. Регистрация обработчиков (handlers)
        dp.include_router(router)

        logger.info("✅ БОТ УСПЕШНО ЗАПУЩЕН И ГОТОВ К РАБОТЕ!")
        
        # Запуск бесконечного цикла опроса Telegram
        await dp.start_polling(bot)
        
    except Exception as e:
        logger.error(f"❌ КРИТИЧЕСКАЯ ОШИБКА ПРИ СТАРТЕ: {e}", exc_info=True)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот остановлен")




