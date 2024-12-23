from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def create_main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➕ Добавить задачу"), KeyboardButton(text="📋 Показать задачи")],
            [KeyboardButton(text="✅ Выполненные задачи"), KeyboardButton(text="❌ Удалить задачу")],
            [KeyboardButton(text="🔗 Поделиться задачами")]
        ],
        resize_keyboard=True
    )


def create_task_keyboard(task_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✏ Редактировать", callback_data=f"edit_{task_id}")],
        [InlineKeyboardButton(text="🔄 Изменить статус", callback_data=f"status_{task_id}")],
        [InlineKeyboardButton(text="✅ Завершить", callback_data=f"done_{task_id}")]
    ])
