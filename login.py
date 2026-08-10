import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor

# .env 파일에 적힌 환경 변수들을 파이썬 메모리로 불러옵니다.
load_dotenv()

app = FastAPI()

# os.getenv()를 사용해 안전하게 변수에 저장합니다.
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

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