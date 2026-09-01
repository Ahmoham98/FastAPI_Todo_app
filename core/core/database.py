from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from core.core.config import settings

engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URL,
    echo=False,  # تو پروداکشن False
    pool_size=10,  # تعداد کانکشن‌های اولیه
    max_overflow=20,  # حداکثر کانکشن اضافه
    pool_pre_ping=True,  # بررسی سلامت کانکشن قبل از استفاده
    pool_recycle=3600,  # بازسازی کانکشن بعد از یک ساعت
)

AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Create base class to declaring tables
Base = declarative_base()

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
