from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.fsm.context import FSMContext
from core.database.requests import set_user, add_task, del_task, task_count
from core.database.requests import get_tasks, check_task_status,change_task, change_status, mark_done
from core.utils.states_form import ToDoStates, STATUS_OPTIONS
# from middlewares import BaseMiddleware
import core.keyboards.keyboards as kb

from pytz import timezone
from datetime import datetime


task = Router()

# user.message.middleware(BaseMiddleware())

@task.callback_query(lambda call: call.data.startswith("edit"))
async def edit_task(callback: CallbackQuery, state: FSMContext):
    _, task_id = callback.data.split("_")
    await state.set_state(ToDoStates.editing_task)
    await state.update_data(task_id=int(task_id))
    await callback.message.answer("Введите новый текст задачи:")

@task.message(ToDoStates.editing_task)
async def editing_task(message: Message, state: FSMContext):
    data = await state.get_data()
    task_id = data.get("task_id")
    new_task = message.text.strip()
    
    if task_id:
        await change_task(task_id,new_task)
        await message.answer("✅ Задача обновлена", reply_markup=kb.create_main_menu())
    else:
        await message.answer("❌ Список задач не найден. Пожалуйста, перезапустите бота командой /start.", reply_markup=kb.create_main_menu())
        await state.clear()   
    
    await state.clear()

@task.callback_query(lambda call: call.data.startswith("status"))
async def set_status(callback: CallbackQuery, state: FSMContext):
    _, task_id = callback.data.split("_")
    await state.set_state(ToDoStates.changing_status)
    await state.update_data(task_id=int(task_id))
    await callback.message.answer("Выберите новый статус задачи:", reply_markup=kb.create_status_keyboard(task_id))


@task.callback_query(lambda call: call.data.startswith("setstatus"))
async def changing_status(callback: CallbackQuery, state: FSMContext):
    data = callback.data.split("_",2)
    _, task_id, status = data
    if status not in STATUS_OPTIONS:
            await callback.message.answer("❌ Некорректный статус.")
            return
    if task_id:
        await change_status(task_id,STATUS_OPTIONS[status])
        await callback.message.answer("✅ Статус изменен")
        await state.clear()
    else:
        await callback.message.answer("❌ Список задач не найден. Пожалуйста, перезапустите бота командой /start.", reply_markup=kb.create_main_menu())
        await state.clear()
    
    await state.clear()


@task.callback_query(lambda call: call.data.startswith("done"))
async def complete_task(callback: CallbackQuery):
    _, task_id = callback.data.split("_")
    if task_id:
        await mark_done(task_id)
        await change_status(task_id,STATUS_OPTIONS["completed"])
        await callback.message.answer("✅ Задача завершена")
    else:
        await callback.message.answer("❌ Список задач не найден. Пожалуйста, перезапустите бота командой /start.", reply_markup=kb.create_main_menu())
