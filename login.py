import os
import base64
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

app = FastAPI()

# DB 환경변수 세팅
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# AES-256 마스터 키 세팅
AES_KEY_STRING = os.getenv("AES_SECRET_KEY")
if not AES_KEY_STRING or len(AES_KEY_STRING) != 32:
    raise ValueError("AES_SECRET_KEY 환경변수가 없거나 길이가 32바이트(글자)가 아닙니다.")
AES_KEY = AES_KEY_STRING.encode('utf-8')


# 클라이언트로부터 입력받을 데이터 형태 (누락되었던 부분 추가)
class UserCreate(BaseModel):
    userid: str
    password: str
    username: str

class UserLogin(BaseModel):
    userid: str
    password: str

def encrypt_password_aes(password: str) -> str:
    """AES-256-GCM 알고리즘으로 비밀번호를 암호화합니다."""
    aesgcm = AESGCM(AES_KEY)
    nonce = os.urandom(12)  # 매번 달라지는 12바이트 난수
    
    # 실제 암호화 진행
    ciphertext = aesgcm.encrypt(nonce, password.encode('utf-8'), None)
    
    # DB 저장을 위해 Base64 문자열로 변환
    encrypted_data = base64.b64encode(nonce + ciphertext).decode('utf-8')
    return encrypted_data

def decrypt_password_aes(encrypted_password: str) -> str:
    """Base64로 저장된 암호문을 받아 원래의 비밀번호(평문)로 복호화합니다."""
    aesgcm = AESGCM(AES_KEY)
    
    # 1. Base64 문자열을 다시 바이트(byte) 형태로 되돌림
    raw_data = base64.b64decode(encrypted_password)
    
    # 2. 앞의 12바이트는 nonce, 나머지는 진짜 암호문으로 분리
    nonce = raw_data[:12]
    ciphertext = raw_data[12:]
    
    try:
        # 3. 복호화 진행
        decrypted_bytes = aesgcm.decrypt(nonce, ciphertext, None)
        # 4. 바이트를 다시 문자열로 변환하여 반환
        return decrypted_bytes.decode('utf-8')
    except Exception:
        raise ValueError("복호화에 실패했습니다. 키가 다르거나 데이터가 손상되었습니다.")

def get_db_connection():
    """PostgreSQL 데이터베이스 연결을 생성하는 함수"""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except Exception as e:
        print(f"DB 연결 실패: {e}")
        return None


@app.get("/users/{userid}")
def get_user_info(userid: str):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="데이터베이스 연결에 실패했습니다.")
    
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        query = """
            SELECT 
                userid,
                password, 
                pre_password, 
                username, 
                login_dt, 
                ip,
                change_password_dt,
                login_try_cnt,
                is_locked,
                is_active,
                refresh_token,
                created_dt,
                updated_dt 
            FROM sqg_users 
            WHERE userid = %s
        """
        
        cursor.execute(query, (userid,))
        user_data = cursor.fetchone()
        
        if not user_data:
            raise HTTPException(status_code=404, detail="해당 유저를 찾을 수 없습니다.")
            
        return user_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


@app.post("/users")
def create_user(user: UserCreate):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="데이터베이스 연결에 실패했습니다.")
    
    try:
        cursor = conn.cursor()
        
        # 1. 입력받은 평문 비밀번호를 암호화 (수정된 부분)
        encrypted_password = encrypt_password_aes(user.password)
        
        query = """
            INSERT INTO sqg_users (userid, password, username, created_dt) 
            VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
        """
        
        # 2. 암호화된 비밀번호를 DB에 전달 (수정된 부분)
        cursor.execute(query, (user.userid, encrypted_password, user.username))
        
        conn.commit()
        
        return {"message": "유저가 성공적으로 생성되었습니다.", "userid": user.userid}

    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        raise HTTPException(status_code=400, detail="이미 존재하는 아이디입니다.")
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


@app.post("/login")
def login(user: UserLogin):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="데이터베이스 연결에 실패했습니다.")
    
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # 1. DB에서 해당 유저의 암호화된 비밀번호를 가져옵니다.
        query = "SELECT password, username FROM sqg_users WHERE userid = %s"
        cursor.execute(query, (user.userid,))
        user_data = cursor.fetchone()
        
        if not user_data:
            raise HTTPException(status_code=401, detail="존재하지 않는 아이디입니다.")
        
        # 2. DB에 저장된 암호를 복호화하여 원래 비밀번호를 알아냅니다.
        decrypted_db_password = decrypt_password_aes(user_data['password'])
        
        # 3. 사용자가 방금 입력한 비밀번호와 DB에서 풀어낸 비밀번호가 같은지 비교합니다.
        if user.password != decrypted_db_password:
            raise HTTPException(status_code=401, detail="비밀번호가 일치하지 않습니다.")
        
        # 로그인 성공 시 응답
        return {
            "message": "로그인 성공!", 
            "username": user_data['username']
        }

    except ValueError as ve:
        raise HTTPException(status_code=500, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()