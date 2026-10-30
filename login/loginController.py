from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from auth import get_session_userid

from login import loginService
from user import userService
from user.userRequest import UserInsertRequest

router = APIRouter(prefix="/login", tags=["Login"])

@router.get("/kakao/process")
async def process_kakao_login(request: Request, db: AsyncSession = Depends(get_db)):
    userid = request.session.get("userid")
    nickname = request.session.get("nickname")
    
    if not userid:
        return RedirectResponse(url="/kakao/login")
        
    client_ip = request.client.host if request.client else "127.0.0.1"
    
    # 1. 회원 여부 조회 및 로그인(업데이트) 처리
    is_member = await loginService.process_login(db, userid, client_ip)
    
    import os
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173").rstrip("/")

    if is_member:
        # 로그인 성공 시 리액트 프론트엔드로 리다이렉트
        return RedirectResponse(url=f"{frontend_url}/")
    else:
        # 2. 회원이 아니면 가입창 제공 (임시로 리액트 회원가입 페이지로 리다이렉트하거나 HTML 응답)
        # 지금은 바로 리액트의 /register 화면 등으로 보내는 것이 좋음. 
        # HTML 창이 구현되어 있으므로 당장은 HTML 창을 띄우거나 리액트 주소로 리다이렉트 가능합니다.
        # 이번에는 간단히 프론트엔드의 /register 페이지로 userid, nickname 파라미터와 함께 넘겨주겠습니다.
        from urllib.parse import urlencode
        params = urlencode({"userid": userid, "nickname": nickname})
        return RedirectResponse(url=f"{frontend_url}/register?{params}")


@router.post("/register")
async def register(
    request: Request,
    username: str = Form(...),
    nickname: str = Form(...),
    phone: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    # 카카오 ID는 폼 값이 아니라 카카오 로그인 세션에서 가져옴 (임의 ID로 가입 방지)
    userid = get_session_userid(request)
    if await userService.get_users(db, userid=userid):
        raise HTTPException(status_code=400, detail="이미 가입된 계정입니다. 다시 로그인해주세요.")

    req = UserInsertRequest(
        userid=userid,
        username=username.strip(),
        nickname=nickname.strip(),
        phone=phone.strip(),
        auth_cd="02" # 02: 일반 사용자
    )

    try:
        linked = await userService.insert_user(db, req)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"회원가입 중 오류가 발생했습니다: {str(e)}")

    # linked=False 이면 관리자가 가입 승인할 때까지 승인 대기
    return {"message": "회원가입이 완료되었습니다.", "linked": linked}

