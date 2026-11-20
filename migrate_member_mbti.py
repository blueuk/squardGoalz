"""
team_member_mbti_l 테이블 생성 스크립트 (풋살 MBTI 결과)
- 멤버별로 필드/골레이 결과를 1건씩 보관하고, 다시 테스트하면 덮어씁니다.
- 테이블이 이미 있으면 아무것도 하지 않습니다.
실행: .\\venv\\Scripts\\python.exe migrate_member_mbti.py
"""
import asyncio
from database import async_session
from sqlalchemy import text

async def migrate():
    async with async_session() as db:
        exists = (await db.execute(text("SELECT to_regclass('public.team_member_mbti_l')"))).scalar()
        if exists:
            print("team_member_mbti_l 테이블이 이미 있어 건너뜁니다.")
            return

        print("team_member_mbti_l 테이블 생성 중...")
        await db.execute(text("""
            CREATE TABLE team_member_mbti_l (
                team_uid VARCHAR(50) NOT NULL,
                member_uid VARCHAR(50) NOT NULL,
                test_type VARCHAR(10) NOT NULL,
                mbti_cd VARCHAR(10) NOT NULL,
                fb_pct INTEGER,
                cw_pct INTEGER,
                pt_pct INTEGER,
                sl_pct INTEGER,
                answers VARCHAR(100),
                question_ver VARCHAR(10),
                create_id VARCHAR(50),
                create_dt TIMESTAMP,
                update_id VARCHAR(50),
                update_dt TIMESTAMP,
                PRIMARY KEY (team_uid, member_uid, test_type)
            );
        """))
        await db.execute(text("COMMENT ON TABLE team_member_mbti_l IS '팀 멤버 풋살 MBTI 결과 리스트'"))
        comments = {
            'test_type': '테스트 종류 (field: 필드, gk: 골레이)',
            'mbti_cd': '유형 코드 (필드 예: FCPL, 골레이 예: G-PS)',
            'fb_pct': 'F 전방 성향 % (100-값 = B 후방, 골레이는 없음)',
            'cw_pct': 'W 측면 성향 % (100-값 = C 중앙, 골레이는 없음)',
            'pt_pct': 'P 파워 성향 % (100-값 = T 테크닉)',
            'sl_pct': 'S 해결 성향 % (100-값 = L 연결)',
            'answers': '문항 번호 순 응답 (1~5)',
            'question_ver': '문항 버전',
        }
        for column, comment in comments.items():
            await db.execute(text(f"COMMENT ON COLUMN team_member_mbti_l.{column} IS '{comment}'"))
        await db.commit()
        print("완료")

if __name__ == "__main__":
    asyncio.run(migrate())
