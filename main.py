import asyncio
import logging
from aiogram import Bot,Dispatcher,F
from aiogram.enums import ContentType, ParseMode
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from core.settings import settings

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

dp = Dispatcher()

@dp.message(Command("help"))
async def help(message: Message):
    await message.answer("Я проверяю функции и возможности библиотеки aiogram и telegram")

async def start():
    logging.basicConfig(level=logging.INFO, 
                    format="%(asctime)s - [%(levelname)s] - %(name)s - "
                    "%(filename)s.%(funcName)s(%(lineno)d) - %(message)s")
     
    bot = Bot(token=settings.bots.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(start())