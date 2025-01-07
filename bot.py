import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F

from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
import os
from app.handlers import setup_bot_commands

from app.handlers import router
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

logging.basicConfig(level=logging.INFO, filename="logs/bot.log", filemode="a",
                    format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


dp.include_router(router)


async def main():
    try:
        await setup_bot_commands(bot)
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")


if __name__ == "__main__":
    asyncio.run(main())
