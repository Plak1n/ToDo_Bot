from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def create_main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➕ Добавить задачу"), KeyboardButton(text="📋 Показать задачи")],
            [KeyboardButton(text="✅ Выполненные задачи"), KeyboardButton(text="❌ Удалить задачу")]
            # [KeyboardButton(text="🔗 Поделиться задачами")]
        ],
        resize_keyboard=True
    )


def create_task_keyboard(task_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✏ Редактировать", callback_data=f"edit_{task_id}")],
        [InlineKeyboardButton(text="🔄 Изменить статус", callback_data=f"status_{task_id}")],
        [InlineKeyboardButton(text="✅ Завершить", callback_data=f"done_{task_id}")]
    ])

def create_status_keyboard(task_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Не начата", callback_data=f"set_status_{task_id}_not_started")],
        [InlineKeyboardButton(text="В работе", callback_data=f"set_status_{task_id}_in_progress")],
        [InlineKeyboardButton(text="Выполнена", callback_data=f"set_status_{task_id}_completed")]
    ])