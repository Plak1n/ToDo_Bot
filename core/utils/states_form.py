from aiogram.fsm.state import State, StatesGroup


class ToDoStates(StatesGroup):
    adding_task = State()
    editing_task = State()
    changing_status = State()
    sharing_task = State()
    deleting_task = State()

