from sqlalchemy import ForeignKey, String, BigInteger, DateTime
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

from core.settings import settings
from datetime import datetime
from pytz import timezone

engine = create_async_engine(url=settings.database.url,
                             echo=True)
    
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)

class Task(Base):
    __tablename__ = 'tasks'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    task: Mapped[str] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(String(50), default="Не выполнена")
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=lambda: (datetime.now(timezone('Europe/Moscow'))).replace(microsecond=0))
    completed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    user:Mapped[int] = mapped_column(ForeignKey('users.id'))


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)