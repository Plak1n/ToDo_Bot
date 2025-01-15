import asyncio
import logging
import signal
from aiogram import Bot,Dispatcher,F
from aiogram.enums import ContentType, ParseMode
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from core.settings import settings
from core.handlers.basic import start_bot, stop_bot
from core.database.user import user
from core.database.task import task
from core.database.models import async_main
from core.utils.commands import set_commands

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

dp = Dispatcher(storage=MemoryStorage())

@dp.message(Command("help"))
async def help(message: Message):
    await message.answer("Привет! Я бот для управления задачами. Для начала работы напишите /start")

async def shutdown(dispatcher: Dispatcher, bot: Bot):
    logging.info("Завершение работы бота...")
    await dispatcher.shutdown()
    await bot.session.close()
    logging.info("Бот завершил работу.")

async def main():
    logging.basicConfig(level=logging.INFO, 
                    format="%(asctime)s - [%(levelname)s] - %(name)s - "
                    "%(filename)s.%(funcName)s(%(lineno)d) - %(message)s")
     
    bot = Bot(token=settings.bots.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    
    dp.include_routers(user,task)
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    
    await async_main()
    await set_commands(bot)
    try:
        await dp.start_polling(bot)
        
    except (KeyboardInterrupt, SystemExit):
        logging.info("Получен сигнал завершения. Завершение работы...")
        await shutdown(dp,bot)

if __name__ == "__main__":
    asyncio.run(main())