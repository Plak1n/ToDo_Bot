from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.fsm.context import FSMContext
from core.database.requests import set_user, add_task
from core.database.requests import get_tasks
from core.utils.states_form import ToDoStates, STATUS_OPTIONS
# from middlewares import BaseMiddleware
import core.keyboards.keyboards as kb

from pytz import timezone
from datetime import datetime


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
            f"{task.id} {task.task}",
            reply_markup=kb.create_task_keyboard(task.id)
        )

@user.message(lambda msg: msg.text == "➕ Добавить задачу")
async def set_task(message: Message, state: FSMContext):
    await message.answer("Введите текст задачи:")
    await state.set_state(ToDoStates.adding_task)

@user.message(ToDoStates.adding_task)
async def process_add_task(message: Message, state: FSMContext):
    
    if not message.from_user.id:
        await message.answer("❌ Ваш список задач не найден. Пожалуйста, перезапустите бота командой /start.", reply_markup=kb.create_main_menu())
        await state.clear()
        return

    task = {
        "task": message.text,
        "status": STATUS_OPTIONS["not_started"],
        "timestamp": datetime.now(timezone('Europe/Moscow'))
    }
    print(message.from_user.id, "121l2;1k")
    await add_task(message.from_user.id, task)
    
    await message.answer(f"✅ Задача добавлена: {task['task']}", reply_markup=kb.create_main_menu())
    await state.clear()