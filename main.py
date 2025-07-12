import asyncio
from aiogram import Bot, Dispatcher, types

import logging
import os

logging.basicConfig(level=logging.INFO)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

@dp.message()
async def echo_handler(message: types.Message) -> None:
    await message.answer(f"Hello! You said: {message.text}")

async def main() -> None:
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
