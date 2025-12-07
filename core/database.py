from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession

import os
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from settings import SQLALCHEMY_DATABASE_URL


engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True if os.getenv('ENV') == 'dev' else False,
    pool_pre_ping=True,
    pool_recycle=3600,
    pool_size=15,
    max_overflow=10,
    pool_timeout=30,
    pool_pre_ping=True,
)

# [AsyncSession]泛型参数确保了类型安全，避免隐式类型转换和潜在的运行时错误。
AsyncSessionLocal = async_sessionmaker[AsyncSession](
    engine,
    class_=AsyncSession,
    expire_on_commit=False,  # 极其重要！防止 commit 后属性访问触发额外的 SQL 查询
)

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            print(e)
            await session.rollback()
        finally:
            await session.close()

SessionDep = Annotated[AsyncSession, Depends(get_db)]
