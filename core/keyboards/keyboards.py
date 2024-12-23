from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from core.database.requests import get_tasks

async def tasks(tg_id):
    tasks = await get_tasks(tg_id)
    keyboard = InlineKeyboardBuilder()
    for task in tasks:
        keyboard.add(InlineKeyboardButton(text=task.task, callback_data=f"task_{task.id}"))
    return keyboard.adjust(1).as_markup()

def create_main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➕ Добавить задачу"), KeyboardButton(text="📋 Показать задачи")],
            [KeyboardButton(text="✅ Выполненные задачи"), KeyboardButton(text="❌ Удалить задачу")],
            [KeyboardButton(text="🔗 Поделиться задачами")]
        ],
        resize_keyboard=True
    )