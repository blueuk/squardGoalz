"""
team_arrange_l 테이블 재생성 스크립트 (vote_uid 단일키 -> team_uid + vote_seq + member_uid 복합키)
기존 테이블에 데이터가 있으면 중단합니다.
실행: .\\venv\\Scripts\\python.exe migrate_team_arrange.py
"""
import asyncio
from database import async_session
from sqlalchemy import text

async def migrate():
    async with async_session() as db:
        exists = (await db.execute(text("SELECT to_regclass('public.team_arrange_l')"))).scalar()
        if exists:
            count = (await db.execute(text("SELECT COUNT(*) FROM team_arrange_l"))).scalar()
            if count:
                print(f"team_arrange_l 에 {count}건의 데이터가 있어 중단합니다.")
                return
            print("빈 team_arrange_l 테이블 삭제 중...")
            await db.execute(text("DROP TABLE team_arrange_l"))

        print("team_arrange_l 테이블 생성 중...")
        await db.execute(text("""
            CREATE TABLE team_arrange_l (
                team_uid VARCHAR(50) NOT NULL,
                vote_seq INTEGER NOT NULL,
                member_uid VARCHAR(50) NOT NULL,
                member_name VARCHAR(50),
                merc_yn VARCHAR(1),
                team_no INTEGER,
                keeper_order INTEGER,
                play_date VARCHAR(8),
                create_id VARCHAR(50),
                create_dt TIMESTAMP,
                update_id VARCHAR(50),
                update_dt TIMESTAMP,
                PRIMARY KEY (team_uid, vote_seq, member_uid)
            );
        """))
        await db.execute(text("COMMENT ON TABLE team_arrange_l IS '팀 배정 리스트'"))
        await db.commit()
        print("완료")

if __name__ == "__main__":
    asyncio.run(migrate())
