import os
import base64
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import httpx

from models import User

AES_KEY_STRING = os.getenv("AES_SECRET_KEY")
if not AES_KEY_STRING or len(AES_KEY_STRING) != 32:
    raise ValueError("AES_SECRET_KEY 오류")
AES_KEY = AES_KEY_STRING.encode('utf-8')

KAKAO_CLIENT_ID = os.getenv("KAKAO_CLIENT_ID")
KAKAO_REDIRECT_URI = os.getenv("KAKAO_REDIRECT_URI")
KAKAO_CLIENT_SECRET = os.getenv("KAKAO_CLIENT_SECRET")


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


async def get_user_by_id(db: AsyncSession, userid: str) -> User | None:
    result = await db.execute(select(User).filter(User.userid == userid))
    return result.scalars().first()

async def create_new_user(db: AsyncSession, userid: str, password: str, username: str) -> User:
    encrypted_password = encrypt_password_aes(password)
    db_user = User(userid=userid, password=encrypted_password, username=username)
    db.add(db_user)
    await db.commit()
    return db_user

async def verify_password(plain_password: str, encrypted_password: str) -> bool:
    try:
        decrypted_db_password = decrypt_password_aes(encrypted_password)
        return plain_password == decrypted_db_password
    except Exception:
        return False

def get_kakao_auth_url() -> str:
    if not KAKAO_CLIENT_ID or not KAKAO_REDIRECT_URI:
        raise ValueError("카카오 설정값(ENV)이 누락되었습니다.")
    return f"https://kauth.kakao.com/oauth/authorize?client_id={KAKAO_CLIENT_ID}&redirect_uri={KAKAO_REDIRECT_URI}&response_type=code"

async def process_kakao_callback(code: str) -> dict:
    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            "https://kauth.kakao.com/oauth/token",
            headers={"Content-type": "application/x-www-form-urlencoded;charset=utf-8"},
            data={
                "grant_type": "authorization_code",
                "client_id": KAKAO_CLIENT_ID,
                "client_secret": KAKAO_CLIENT_SECRET,
                "redirect_uri": KAKAO_REDIRECT_URI,
                "code": code
            }
        )
        token_data = token_response.json()
        access_token = token_data.get("access_token")
        if not access_token:
            raise ValueError(f"토큰 발급 실패: {token_data}")

        user_info_response = await client.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}",
                     "Content-type": "application/x-www-form-urlencoded;charset=utf-8"}
        )
        user_info = user_info_response.json()
        
    kakao_id = user_info.get("id")
    if not kakao_id:
        raise ValueError(f"유저 정보 조회 실패: {user_info}")

    return {"db_userid": f"kakao_{kakao_id}"}

