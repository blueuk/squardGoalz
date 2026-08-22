import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

# 비동기 통신을 위해 postgresql+asyncpg 드라이버를 사용합니다.
SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

# echo=True 설정으로 SQL 쿼리 로그를 출력합니다.
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)

# 비동기 세션을 생성하는 팩토리
async_session = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
)

Base = declarative_base()

async def get_db():
    """FastAPI 의존성 주입(Dependency Injection)을 위한 비동기 DB 세션 함수"""
    async with async_session() as session:
        yield session