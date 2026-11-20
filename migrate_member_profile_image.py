"""
member_profile_image_l 테이블 생성 스크립트 (프로필 사진)
- 멤버별로 브라우저에서 256x256으로 줄인 사진 1장을 보관하고, 바꾸면 덮어씁니다.
- 테이블이 이미 있으면 아무것도 하지 않습니다.
실행: .\\venv\\Scripts\\python.exe migrate_member_profile_image.py
"""
import asyncio
from database import async_session
from sqlalchemy import text

async def migrate():
    async with async_session() as db:
        exists = (await db.execute(text("SELECT to_regclass('public.member_profile_image_l')"))).scalar()
        if exists:
            print("member_profile_image_l 테이블이 이미 있어 건너뜁니다.")
            return

        print("member_profile_image_l 테이블 생성 중...")
        await db.execute(text("""
            CREATE TABLE member_profile_image_l (
                team_uid VARCHAR(50) NOT NULL,
                member_uid VARCHAR(50) NOT NULL,
                image BYTEA NOT NULL,
                content_type VARCHAR(30) NOT NULL,
                image_size INTEGER,
                create_id VARCHAR(50),
                create_dt TIMESTAMP,
                update_id VARCHAR(50),
                update_dt TIMESTAMP,
                PRIMARY KEY (team_uid, member_uid)
            );
        """))
        await db.execute(text("COMMENT ON TABLE member_profile_image_l IS '멤버 프로필 사진 리스트 (브라우저에서 256x256으로 줄인 이미지)'"))
        await db.execute(text("COMMENT ON COLUMN member_profile_image_l.image IS '이미지 바이너리'"))
        await db.execute(text("COMMENT ON COLUMN member_profile_image_l.content_type IS '이미지 형식 (image/webp, image/jpeg, image/png)'"))
        await db.execute(text("COMMENT ON COLUMN member_profile_image_l.image_size IS '이미지 크기 (byte)'"))
        await db.commit()
        print("완료")

if __name__ == "__main__":
    asyncio.run(migrate())
