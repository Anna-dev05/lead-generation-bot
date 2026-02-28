import sys
import os

# Добавляем все возможные пути в память бота
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app'))

from app.config import load_config
from app.handlers import router
from app.sheets import get_worksheet
from app.database import init_db


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