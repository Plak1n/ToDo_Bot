from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

from core.database.requests import set_user, del_task, set_task
# from middlewares import BaseMiddleware

import core.keyboards.keyboards as kb
from core.database.requests import get_tasks

user = Router()

# user.message.middleware(BaseMiddleware())

@user.message(CommandStart())
async def cmd_start(message: Message):
    await set_user(message.from_user.id)
    # await message.answer('Нажмите на выполненную задачу чтобы удалить или напишите новую в чат',
    #                      reply_markup=await kb.tasks(message.from_user.id))
    await message.answer('Привет! Я бот для управления задачами. Выберите действие из меню:',
                         reply_markup=kb.create_main_menu())


@user.message(lambda msg: msg.text == "📋 Показать задачи")
async def tasks(message: Message):
    tasks = await get_tasks(message.from_user.id)
    if not tasks:
        await message.answer("📭 Список задач пуст или не найден. Добавьте новую задачу.", reply_markup=kb.create_main_menu())
        return
    keyboard = InlineKeyboardBuilder()
    for task in tasks:
        await message.answer(
            f"📌 {task.task}",
            reply_markup=kb.create_task_keyboard(task.id)
        )


# @user.callback_query(F.data.startswith('task_'))
# async def delete_task(callback:CallbackQuery):
#     await del_task(callback.data.split('_')[1])
#     await callback.answer('Задача выполнена')
#     await callback.message.delete()
#     await callback.message.answer('Нажмите на выполненную задачу чтобы удалить или напишите новую в чат',
#                          reply_markup=await kb.tasks(callback.from_user.id))
    


# @user.message("Pass")
# async def add_task(message: Message):
#     if len(message.text) > 100:
#         await message.answer('Задача слишком длинная')
#         return
#     await set_task(message.from_user.id, message.text)
#     await message.answer('Задача добавлена')
#     await message.answer('Нажмите на выполненную задачу чтобы удалить или напишите новую в чат',
#                          reply_markup=await kb.tasks(message.from_user.id))
    