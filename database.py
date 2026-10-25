import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv

load_dotenv(override=True)

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

# 비동기 통신을 위해 postgresql+asyncpg 드라이버를 사용합니다.
SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

# 성능 최적화:
# 1. echo=False 로 I/O 로깅 병목 제거
# 2. pool_size=20, max_overflow=20 으로 동시 요청 시 큐 대기 방지
# 3. pool_pre_ping=True 로 유휴 끊김 방지
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, 
    echo=False, 
    future=True,
    pool_size=20,
    max_overflow=20,
    pool_timeout=30,
    pool_pre_ping=True,
    pool_recycle=1800
)

# 비동기 세션을 생성하는 팩토리
async_session = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
)

Base = declarative_base()

async def get_db():
    """FastAPI 의존성 주입(Dependency Injection)을 위한 비동기 DB 세션 함수"""
    async with async_session() as session:
        yield session
