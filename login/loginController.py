from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db

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
    
    if is_member:
        return HTMLResponse(f"""
        <html>
            <body style="font-family: Arial; text-align: center; margin-top: 50px;">
                <h2>🎉 로그인 성공!</h2>
                <p>스쿼드 골츠에 다시 오신 것을 환영합니다!</p>
            </body>
        </html>
        """)
    else:
        # 2. 회원이 아니라면 가입 폼 제공
        return HTMLResponse(f"""
        <html>
            <head>
                <meta charset="UTF-8">
                <title>추가 정보 입력</title>
            </head>
            <body style="font-family: Arial; text-align: center; margin-top: 50px;">
                <h2>⚽ 스쿼드 골츠 회원가입</h2>
                <p>카카오 인증이 완료되었습니다. 서비스 이용을 위해 추가 정보를 입력해주세요!</p>
                
                <form action="/login/register" method="POST" style="margin-top: 20px;">
                    <input type="hidden" name="userid" value="{userid}">
                    
                    <div style="margin-bottom: 10px;">
                        <label>이름(실명): <input type="text" name="username" required></label>
                    </div>
                    <div style="margin-bottom: 10px;">
                        <label>닉네임: <input type="text" name="nickname" value="{nickname}" required></label>
                    </div>
                    <div style="margin-bottom: 10px;">
                        <label>전화번호: <input type="text" name="phone" placeholder="010-1234-5678" required></label>
                    </div>
                    
                    <button type="submit" style="padding: 10px 20px; font-size: 16px; background-color: #FEE500; border: none; cursor: pointer; font-weight: bold; margin-top: 10px;">가입 완료하기</button>
                </form>
            </body>
        </html>
        """)

@router.post("/register")
async def register(
    userid: str = Form(...),
    username: str = Form(...),
    nickname: str = Form(...),
    phone: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    # 가입 폼에서 넘어온 정보를 user/insert 로직을 이용해 등록
    req = UserInsertRequest(
        userid=userid,
        username=username,
        nickname=nickname,
        phone=phone,
        auth_cd="02" # 02: 일반 사용자
    )
    
    await userService.insert_user(db, req)
    
    return HTMLResponse(f"""
    <html>
        <body style="font-family: Arial; text-align: center; margin-top: 50px;">
            <h2>🎉 회원가입 완료!</h2>
            <p>{nickname}님, 스쿼드 골츠의 멤버가 되신 것을 환영합니다!</p>
            <a href="/login/kakao/process" style="display:inline-block; margin-top: 20px; padding: 10px; background:#ddd; text-decoration:none; color:black;">로그인 하러가기</a>
        </body>
    </html>
    """)

