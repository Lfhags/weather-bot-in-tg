from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import BigInteger, String
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url='sqlite+aiosqlite:///db_weather.sqlite3')

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    region = mapped_column(String, nullable=True)
    time = mapped_column(String, nullable=True)

class Region(Base):
    __tablename__ = 'Regions'
    id: Mapped[int] = mapped_column(primary_key=True)
    region = mapped_column(String)

class Time(Base):
    __tablename__ = 'Times'
    id: Mapped[int] = mapped_column(primary_key=True)
    time = mapped_column(String)

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
