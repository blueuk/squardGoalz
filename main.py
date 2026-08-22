from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import engine, Base
from login.login import router as login_router

# 앱 생명주기 관리 (시작 및 종료 시 DB 연결/해제 설정)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 앱 시작 시 실행될 로직
    # 주의: Alembic으로 마이그레이션을 관리한다면 아래 주석 처리된 부분은 사용하지 않는 것이 좋습니다.
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)
    yield
    # 앱 종료 시 실행될 로직
    await engine.dispose()

# 메인 앱 생성 (lifespan 연동)
app = FastAPI(title="Squard Goalz API", lifespan=lifespan)

# 라우터 연결
app.include_router(login_router)

@app.get("/")
async def root():
    return {"message": "Welcome to Squard Goalz API!"}