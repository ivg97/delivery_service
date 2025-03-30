from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import settings


async_engine = create_async_engine(settings.db_url, echo=True)


async_session = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()


async def get_session():
    async with async_session() as session:
        yield session
