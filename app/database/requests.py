from sqlalchemy import select
from .models import User, Region, Time, async_session

async def set_user(tg_id: int):
    async with async_session() as session:
        query = select(User).where(User.tg_id == tg_id)
        result = await session.execute(query)
        user = result.scalar_one_or_none()
        
        if not user:
            user = User(tg_id=tg_id)
            session.add(user)
            await session.commit()


async def get_region(tg_id: int):
    async with async_session() as session:
        query = select(User).where(User.tg_id == tg_id)
        result = await session.execute(query)
        user = result.scalar_one_or_none()
        
        if not user:
            return None
        return user.region
    

async def get_time(tg_id: int):
    async with async_session() as session:
        query = select(User).where(User.tg_id == tg_id)
        result = await session.execute(query)
        user = result.scalar_one_or_none()
        
        if not user:
            return None
        return user.time

async def set_region(tg_id: int, region: str):
    async with async_session() as session:
        query = select(User).where(User.tg_id == tg_id)
        result = await session.execute(query)
        user = result.scalar_one_or_none()
        
        if user:
            user.region = region
            await session.commit()
            return True
        return False

async def set_time(tg_id: int, time: str):
    async with async_session() as session:
        query = select(User).where(User.tg_id == tg_id)
        result = await session.execute(query)
        user = result.scalar_one_or_none()
        
        if user:
            user.time = time
            await session.commit()
            return True
        return False