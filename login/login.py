import os
import base64
from fastapi import APIRouter, HTTPException, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import requests

from database import get_db
from models import User

router = APIRouter()

AES_KEY_STRING = os.getenv("AES_SECRET_KEY")
if not AES_KEY_STRING or len(AES_KEY_STRING) != 32:
    raise ValueError("AES_SECRET_KEY 오류")
AES_KEY = AES_KEY_STRING.encode('utf-8')

KAKAO_CLIENT_ID = os.getenv("KAKAO_CLIENT_ID")
KAKAO_REDIRECT_URI = os.getenv("KAKAO_REDIRECT_URI")

class UserCreate(BaseModel):
    userid: str = Field(min_length=4, max_length=15)
    password: str = Field(min_length=8, max_length=100)
    username: str = Field(min_length=2, max_length=10)
    model_config = ConfigDict(json_schema_extra={"example": {"userid": "Woogi", "password": "my_secret_password_123!", "username": "우기"}})

class UserLogin(BaseModel):
    userid: str
    password: str
    model_config = ConfigDict(json_schema_extra={"example": {"userid": "Woogi", "password": "my_secret_password_123!"}})

def encrypt_password_aes(password: str) -> str:
    aesgcm = AESGCM(AES_KEY)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, password.encode('utf-8'), None)
    return base64.b64encode(nonce + ciphertext).decode('utf-8')

def decrypt_password_aes(encrypted_password: str) -> str:
    aesgcm = AESGCM(AES_KEY)
    raw_data = base64.b64decode(encrypted_password)
    nonce = raw_data[:12]
    ciphertext = raw_data[12:]
    return aesgcm.decrypt(nonce, ciphertext, None).decode('utf-8')

@router.get("/users/{userid}")
def get_user_info(userid: str, db: Session = Depends(get_db)):
    user_data = db.query(User).filter(User.userid == userid).first()
    if not user_data:
        raise HTTPException(status_code=404, detail="해당 유저를 찾을 수 없습니다.")
    return user_data

@router.post("/users")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.userid == user.userid).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="이미 존재하는 아이디입니다.")

    encrypted_password = encrypt_password_aes(user.password)
    db_user = User(userid=user.userid, password=encrypted_password, username=user.username)
    
    try:
        db.add(db_user)
        db.commit()
        return {"message": "유저가 성공적으로 생성되었습니다.", "userid": db_user.userid}
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="회원가입 중 오류가 발생했습니다.")

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    user_data = db.query(User).filter(User.userid == user.userid).first()
    if not user_data:
        raise HTTPException(status_code=401, detail="존재하지 않는 아이디입니다.")
    
    try:
        decrypted_db_password = decrypt_password_aes(user_data.password)
    except Exception:
        raise HTTPException(status_code=500, detail="비밀번호 복호화 오류")
        
    if user.password != decrypted_db_password:
        raise HTTPException(status_code=401, detail="비밀번호가 일치하지 않습니다.")
    
    return {"message": "로그인 성공!", "username": user_data.username}

@router.get("/kakao/login")
def kakao_login():
    """카카오 로그인 창으로 유저를 보냅니다."""
    # 환경변수가 잘 들어왔는지 확인
    if not KAKAO_CLIENT_ID or not KAKAO_REDIRECT_URI:
        raise HTTPException(status_code=500, detail="카카오 설정값(ENV)이 누락되었습니다. .env 파일을 확인해주세요.")
        
    kakao_auth_url = f"https://kauth.kakao.com/oauth/authorize?client_id={KAKAO_CLIENT_ID}&redirect_uri={KAKAO_REDIRECT_URI}&response_type=code"
    return RedirectResponse(url=kakao_auth_url)

@router.get("/kakao/callback", response_class=HTMLResponse)
def kakao_callback(code: str, db: Session = Depends(get_db)):
    token_response = requests.post(
        "https://kauth.kakao.com/oauth/token",
        headers={"Content-type": "application/x-www-form-urlencoded;charset=utf-8"},
        data={
            "grant_type": "authorization_code",
            "client_id": KAKAO_CLIENT_ID,
            "redirect_uri": KAKAO_REDIRECT_URI,
            "code": code
        }
    )
    token_data = token_response.json()
    access_token = token_data.get("access_token")
    if not access_token:
        raise HTTPException(status_code=400, detail=f"토큰 발급 실패: {token_data}")

    user_info_response = requests.get(
        "https://kapi.kakao.com/v2/user/me",
        headers={"Authorization": f"Bearer {access_token}",
                 "Content-type": "application/x-www-form-urlencoded;charset=utf-8"}
    )
    user_info = user_info_response.json()
    kakao_id = user_info.get("id")
    if not kakao_id:
        raise HTTPException(status_code=400, detail=f"유저 정보 조회 실패: {user_info}")

    db_userid = f"kakao_{kakao_id}"
    existing_user = db.query(User).filter(User.userid == db_userid).first()

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
def kakao_register(userid: str = Form(...), realname: str = Form(...), db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.userid == userid).first()
    if existing_user:
        return {"message": "이미 가입된 회원입니다.", "username": existing_user.username}

    random_pw = encrypt_password_aes(f"{userid}_secret_pw!")
    new_user = User(
        userid=userid,
        password=random_pw,
        username=realname
    )
    
    db.add(new_user)
    db.commit()

    return {
        "message": "회원가입 및 실명 등록 성공!",
        "userid": userid,
        "username": realname
    }