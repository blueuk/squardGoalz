import os
import base64
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# ORM용 함수와 모델 가져오기
from database import get_db
from models import User

router = APIRouter()

AES_KEY_STRING = os.getenv("AES_SECRET_KEY")
if not AES_KEY_STRING or len(AES_KEY_STRING) != 32:
    raise ValueError("AES_SECRET_KEY 오류")
AES_KEY = AES_KEY_STRING.encode('utf-8')

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
    # 아이디 중복 체크
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