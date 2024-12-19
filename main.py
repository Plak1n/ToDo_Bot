import asyncio
import logging
import signal
from aiogram import Bot,Dispatcher,F
from aiogram.enums import ContentType, ParseMode
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from core.settings import settings
from core.handlers.basic import start_bot, stop_bot
from core.database.user import user
from core.database.models import async_main

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

dp = Dispatcher()

@dp.message(Command("help"))
async def help(message: Message):
    await message.answer("Я проверяю функции и возможности библиотеки aiogram и telegram")

async def shutdown(dispatcher: Dispatcher, bot: Bot):
    logging.info("Завершение работы бота...")
    await dispatcher.shutdown()
    await bot.session.close()
    logging.info("Бот завершил работу.")

async def start():
    logging.basicConfig(level=logging.INFO, 
                    format="%(asctime)s - [%(levelname)s] - %(name)s - "
                    "%(filename)s.%(funcName)s(%(lineno)d) - %(message)s")
     
    bot = Bot(token=settings.bots.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    
    dp.include_routers(user)
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    
    try:
        await dp.start_polling(bot)
    except (KeyboardInterrupt, SystemExit):
        logging.info("Получен сигнал завершения. Завершение работы...")
    finally:
        await shutdown(dp,bot)

if __name__ == "__main__":
    asyncio.run(start())