from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "postgresql+asyncpg://user:password@localhost/Todoappasync"

# CREATES ASYNC ENGINE
engine = create_async_engine(
    DATABASE_URL,
    echo=False,  # تو پروداکشن False بذار
    pool_size=10,  # تعداد کانکشن‌های اولیه
    max_overflow=20,  # حداکثر کانکشن اضافه
    pool_pre_ping=True,  # بررسی سلامت کانکشن قبل از استفاده
    pool_recycle=3600,  # بازسازی کانکشن بعد از یک ساعت
)
# SESSION FACTORY
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()

# FOR GETTING SESISON AS DEPENEDENCY
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



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())