from core.database.models import async_session
from core.database.models import User, Task
from sqlalchemy import select, update, delete, desc, func
from sqlalchemy.exc import SQLAlchemyError


async def set_user(tg_id):
    async with async_session() as session:
        try:
            user = await session.scalar(select(User).where(User.tg_id == tg_id))
            
            if not user:
                session.add(User(tg_id=tg_id))
                await session.commit()
        except SQLAlchemyError as e:
            print(f"An error occurred in set user: {e}")
            await session.rollback()

async def get_tasks(tg_id):
    async with async_session() as session:
        try:
            user = await session.scalar(select(User).where(User.tg_id == tg_id))
            if not user:
                return
            tasks = await session.scalars(select(Task).where(Task.user == user.id))
            
            return tasks
        except SQLAlchemyError as e:
            print(f"An error occurred in get tasks: {e}")
            await session.rollback()
            return


async def task_count(tg_id):
    async with async_session() as session:
        try:
            user = await session.scalar(select(User).where(User.tg_id == tg_id))
            if not user:
                return

            return await session.scalar(select(func.count(Task.id)).where(Task.user == user.id))
        except SQLAlchemyError as e:
            print(f"An error occurred in task: {e}")
            await session.rollback()


async def add_task(tg_id, task:dict):
    async with async_session() as session:
        try:
            user = await session.scalar(select(User).where(User.tg_id == tg_id))
            if not user:
                return
            
            session.add(Task(task=task['task'], status=task['status'], timestamp=task['timestamp'], user=user.id))
            await session.commit()
        except SQLAlchemyError as e:
            print(f"An error occurred in add_task: {e}")
            await session.rollback()


async def del_task(task_id):
    async with async_session() as session:
        try:
            await session.execute(delete(Task).where(Task.id == task_id))
            await session.commit()
        except SQLAlchemyError as e:
            print(f"An error occurred in del_task: {e}")
            await session.rollback()
        

async def check_task_status(task_id):
    async with async_session() as session:
            try:
                task = await session.scalar(select(Task).where(Task.id == task_id))
                
                if not task:
                    return
                
                return task.status
            except SQLAlchemyError as e:
                print(f"An error occurred in check_task_status: {e}")
                await session.rollback()


async def change_task(task_id, task_text):
    async with async_session() as session:
        try:
            await session.execute(
                update(Task)
                .where(Task.id == task_id)
                .values(task=task_text)
            )
            await session.commit()
        except SQLAlchemyError as e:
            print(f"An error occurred in change_task: {e}")
            await session.rollback()


async def change_stauts(task_id, task_status):
    async with async_session() as session:
        try:
            await session.execute(
                update(Task)
                .where(Task.id == task_id)
                .values(status=task_status)
            )
            await session.commit()
        except SQLAlchemyError as e:
            print(f"An error occurred in change_task: {e}")
            await session.rollback()