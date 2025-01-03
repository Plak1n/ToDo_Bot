from core.database.models import async_session
from core.database.models import User, Task
from sqlalchemy import select, update, delete, desc, func


async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        
        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()


async def get_tasks(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            return
        tasks = await session.scalars(select(Task).where(Task.user == user.id))
        
        return tasks  


async def task_count(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            return

        return await session.scalar(select(func.count(Task.id)).where(Task.user == user.id))


async def add_task(tg_id, task:dict):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            return
        
        session.add(Task(task=task['task'], status=task['status'], timestamp=task['timestamp'], user=user.id))
        await session.commit()


async def del_task(task_id):
    async with async_session() as session:
        await session.execute(delete(Task).where(Task.id == task_id))
        await session.commit()
        

async def check_task_status(task_id):
    async with async_session() as session:
        task = await session.scalar(select(Task).where(Task.id == task_id))
        
        if not task:
            return
        
        return task.status