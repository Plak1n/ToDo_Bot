from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

from core.database.requests import set_user
# from middlewares import BaseMiddleware

import core.keyboards.keyboards as kb

user = Router()

# user.message.middleware(BaseMiddleware())

@user.message(CommandStart())
async def cmd_start(message: Message):
    await set_user(message.from_user.id)
    await message.answer('Нажмите на выполненную задачу чтобы удалить или напишите новую в чат',
                         reply_markup=await kb.tasks(message.from_user.id))