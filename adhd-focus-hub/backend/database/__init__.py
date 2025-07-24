from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")

engine = create_async_engine(DATABASE_URL, echo=False)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

class Base(DeclarativeBase):
    pass

async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session
