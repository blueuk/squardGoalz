"""
auth_role_permission_l 테이블 생성 및 기본 권한 등록 스크립트
- 테이블이 없으면 생성합니다.
- 데이터가 비어 있을 때만 일반(02) 역할에 기존 동작과 같은 기본 권한을 넣습니다.
  (기존에도 일반 회원이 오늘 이후 일정 수정 / 팀원 투표 변경 가능)
실행: .\\venv\\Scripts\\python.exe migrate_permission.py
"""
import asyncio
from datetime import datetime
from database import async_session
from sqlalchemy import text

DEFAULT_GRANTS = {
    '02': ['schedule.manage', 'vote.manage'],
}

async def migrate():
    async with async_session() as db:
        print("auth_role_permission_l 테이블 확인/생성 중...")
        await db.execute(text("""
            CREATE TABLE IF NOT EXISTS auth_role_permission_l (
                auth_cd VARCHAR(10) NOT NULL,
                perm_cd VARCHAR(50) NOT NULL,
                create_id VARCHAR(50),
                create_dt TIMESTAMP,
                PRIMARY KEY (auth_cd, perm_cd)
            );
        """))
        await db.execute(text("COMMENT ON TABLE auth_role_permission_l IS '역할별 기능 권한 리스트'"))

        count = (await db.execute(text("SELECT COUNT(*) FROM auth_role_permission_l"))).scalar()
        if count:
            print(f"이미 {count}건의 권한 데이터가 있어 기본 권한 등록은 건너뜁니다.")
        else:
            now = datetime.now()
            for auth_cd, perm_cds in DEFAULT_GRANTS.items():
                for perm_cd in perm_cds:
                    await db.execute(text("""
                        INSERT INTO auth_role_permission_l (auth_cd, perm_cd, create_id, create_dt)
                        VALUES (:auth_cd, :perm_cd, 'system', :now)
                    """), {'auth_cd': auth_cd, 'perm_cd': perm_cd, 'now': now})
                print(f"  {auth_cd}: {', '.join(perm_cds)}")
        await db.commit()
        print("완료")

if __name__ == "__main__":
    asyncio.run(migrate())
