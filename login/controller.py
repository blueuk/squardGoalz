from fastapi import APIRouter, HTTPException, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from login.request import UserCreate, UserLogin
from login.response import UserResponse, MessageResponse
from login import service

router = APIRouter()

@router.get("/users/{userid}", response_model=UserResponse)
async def get_user_info(userid: str, db: AsyncSession = Depends(get_db)):
    user_data = await service.get_user_by_id(db, userid)
    if not user_data:
        raise HTTPException(status_code=404, detail="해당 유저를 찾을 수 없습니다.")
    return UserResponse(userid=user_data.userid, username=user_data.username)

@router.post("/users", response_model=MessageResponse)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    existing_user = await service.get_user_by_id(db, user.userid)
    if existing_user:
        raise HTTPException(status_code=400, detail="이미 존재하는 아이디입니다.")

    try:
        new_user = await service.create_new_user(db, user.userid, user.password, user.username)
        return MessageResponse(message="유저가 성공적으로 생성되었습니다.", userid=new_user.userid)
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=500, detail="회원가입 중 오류가 발생했습니다.")

@router.post("/login", response_model=MessageResponse)
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    user_data = await service.get_user_by_id(db, user.userid)
    if not user_data:
        raise HTTPException(status_code=401, detail="존재하지 않는 아이디입니다.")
    
    is_valid = await service.verify_password(user.password, user_data.password)
    if not is_valid:
        raise HTTPException(status_code=401, detail="비밀번호가 일치하지 않거나 복호화 오류입니다.")
    
    return MessageResponse(message="로그인 성공!", username=user_data.username)

@router.get("/kakao/login")
async def kakao_login():
    """카카오 로그인 창으로 유저를 보냅니다."""
    try:
        url = service.get_kakao_auth_url()
        return RedirectResponse(url=url)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/kakao/callback", response_class=HTMLResponse)
async def kakao_callback(code: str, db: AsyncSession = Depends(get_db)):
    try:
        kakao_data = await service.process_kakao_callback(code)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
        
    db_userid = kakao_data["db_userid"]
    existing_user = await service.get_user_by_id(db, db_userid)

    if existing_user:
        return f"""
        <html>
            <body style="font-family: Arial; text-align: center; margin-top: 50px;">
                <h2>🎉 로그인 성공!</h2>
                <p>환영합니다, <b>{existing_user.username}</b>님!</p>
            </body>
        </html>
        """

    return f"""
    <html>
        <head>
            <meta charset="UTF-8">
            <title>추가 정보 입력</title>
        </head>
        <body style="font-family: Arial; text-align: center; margin-top: 50px;">
            <h2>⚽ 스쿼드 골츠 회원가입</h2>
            <p>카카오 인증이 완료되었습니다. 서비스에서 사용할 <b>실명(이름)</b>을 입력해주세요!</p>
            
            <form action="/kakao/register" method="POST" style="margin-top: 20px;">
                <input type="hidden" name="userid" value="{db_userid}">
                <input type="text" name="realname" placeholder="실명을 입력하세요 (예: 홍길동)" required style="padding: 10px; width: 250px; font-size: 16px;">
                <br><br>
                <button type="submit" style="padding: 10px 20px; font-size: 16px; background-color: #FEE500; border: none; cursor: pointer; font-weight: bold;">가입 완료하기</button>
            </form>
        </body>
    </html>
    """

@router.post("/kakao/register")
async def kakao_register(userid: str = Form(...), realname: str = Form(...), db: AsyncSession = Depends(get_db)):
    existing_user = await service.get_user_by_id(db, userid)
    if existing_user:
        return {"message": "이미 가입된 회원입니다.", "username": existing_user.username}

    new_user = await service.create_new_user(db, userid, f"{userid}_secret_pw!", realname)

    return {
        "message": "회원가입 및 실명 등록 성공!",
        "userid": new_user.userid,
        "username": new_user.username
    }

