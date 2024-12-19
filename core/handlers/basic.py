from aiogram import Bot
from aiogram.types import Message
from core.settings import settings


async def start_bot(bot: Bot):
    await bot.send_message(settings.bots.bot_owner_id, text="Бот запущен")
    
async def stop_bot(bot: Bot):
    await bot.send_message(settings.bots.bot_owner_id, text="Бот остановлен")