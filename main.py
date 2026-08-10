from fastapi import FastAPI
# login 폴더 안의 login.py 파일에서 router를 가져옵니다.
from login.login import router as login_router

# 메인 앱 생성
app = FastAPI(title="Squard Goalz API")

# 분리했던 로그인 라우터를 메인 앱에 찰칵! 하고 조립합니다.
app.include_router(login_router)