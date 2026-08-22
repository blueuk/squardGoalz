import os
from starlette.middleware.sessions import SessionMiddleware
from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import engine, Base
from user.userController import router as user_router
from kakao.kakaoController import router as kakao_router
from login.loginController import router as login_router
from common_cd.commonCdController import router as common_cd_router
from position_point.positionController import router as position_router
from teamInfo.teamInfoController import router as team_info_router
from teamMember.teamMemberController import router as team_member_router
from teamAccount.teamAccountController import router as team_account_router
from teamArrange.teamArrangeController import router as team_arrange_router
from memberScore.memberScoreController import router as member_score_router
from payment.paymentController import router as payment_router
from record.recordController import router as record_router
from schedule.scheduleController import router as schedule_router
from stardium.stardiumController import router as stardium_router
from vote.voteController import router as vote_router
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

# 세션 미들웨어 등록 (세션 쿠키 관리에 필요)
app.add_middleware(
    SessionMiddleware, 
    secret_key=os.getenv("AES_SECRET_KEY", "default-secret-key-for-session")
)

# 라우터 연결
app.include_router(user_router)
app.include_router(kakao_router)
app.include_router(login_router)
app.include_router(common_cd_router)
app.include_router(position_router)
app.include_router(team_info_router)
app.include_router(team_member_router)
app.include_router(team_account_router)
app.include_router(team_arrange_router)
app.include_router(member_score_router)
app.include_router(payment_router)
app.include_router(record_router)
app.include_router(schedule_router)
app.include_router(stardium_router)
app.include_router(vote_router)

@app.get("/")
async def root():
    return {"message": "Welcome to Squard Goalz API!"}