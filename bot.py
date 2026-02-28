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

