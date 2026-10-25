"""
포지션 공통코드 & 가중치 데이터 seed 스크립트
실행: .\venv\Scripts\python.exe seed_position.py
"""
import asyncio
from datetime import datetime
from database import engine, async_session
from sqlalchemy import text

POSITIONS = [
    {'code': 'FIX', 'code_name': '픽소',    'seq': 1},
    {'code': 'PIV', 'code_name': '피보',    'seq': 2},
    {'code': 'ALA', 'code_name': '아라',    'seq': 3},
    {'code': 'GOL', 'code_name': '골레이로', 'seq': 4},
    {'code': 'CEN', 'code_name': '센트로',  'seq': 5},
]

WEIGHTS = {
    'GOL': {'001':0.008,'002':0.008,'003':0.023,'004':0.008,'005':0.008,'006':0.023,'007':0.115,'008':0.057,'009':0.115,'010':0.008,'011':0.008,'012':0.115,'013':0.008,'014':0.023,'015':0.115,'016':0.023,'017':0.008,'018':0.008,'019':0.008,'020':0.002,'021':0.008,'022':0.008,'023':0.057,'024':0.057,'025':0.057,'026':0.008,'027':0.057,'028':0.057},
    'FIX': {'001':0.043,'002':0.043,'003':0.017,'004':0.006,'005':0.043,'006':0.043,'007':0.043,'008':0.017,'009':0.087,'010':0.087,'011':0.043,'012':0.087,'013':0.087,'014':0.043,'015':0.006,'016':0.017,'017':0.087,'018':0.006,'019':0.006,'020':0.008,'021':0.006,'022':0.006,'023':0.043,'024':0.043,'025':0.043,'026':0.006,'027':0.017,'028':0.017},
    'ALA': {'001':0.006,'002':0.092,'003':0.092,'004':0.092,'005':0.006,'006':0.004,'007':0.046,'008':0.046,'009':0.018,'010':0.018,'011':0.018,'012':0.006,'013':0.006,'014':0.018,'015':0.006,'016':0.006,'017':0.018,'018':0.092,'019':0.046,'020':0.046,'021':0.046,'022':0.046,'023':0.046,'024':0.006,'025':0.046,'026':0.092,'027':0.018,'028':0.018},
    'PIV': {'001':0.099,'002':0.099,'003':0.020,'004':0.007,'005':0.006,'006':0.006,'007':0.050,'008':0.050,'009':0.099,'010':0.006,'011':0.006,'012':0.006,'013':0.006,'014':0.006,'015':0.007,'016':0.050,'017':0.006,'018':0.007,'019':0.050,'020':0.050,'021':0.099,'022':0.099,'023':0.050,'024':0.006,'025':0.020,'026':0.050,'027':0.020,'028':0.020},
    'CEN': {'001':0.006,'002':0.049,'003':0.049,'004':0.006,'005':0.006,'006':0.006,'007':0.049,'008':0.020,'009':0.098,'010':0.020,'011':0.049,'012':0.020,'013':0.006,'014':0.020,'015':0.006,'016':0.007,'017':0.006,'018':0.006,'019':0.098,'020':0.049,'021':0.006,'022':0.006,'023':0.098,'024':0.049,'025':0.098,'026':0.020,'027':0.098,'028':0.049},
}

async def seed():
    async with async_session() as db:
        now = datetime.now()
        
        # 0. 테이블 생성 (없는 경우)
        print("position_point_b 테이블 확인/생성 중...")
        await db.execute(text("""
            CREATE TABLE IF NOT EXISTS position_point_b (
                position_cd VARCHAR(50) NOT NULL,
                score_cd VARCHAR(20) NOT NULL,
                position_val NUMERIC(10, 4),
                create_id VARCHAR(50),
                create_dt TIMESTAMP,
                update_id VARCHAR(50),
                update_dt TIMESTAMP,
                PRIMARY KEY (position_cd, score_cd)
            );
        """))
        await db.commit()

        # 1. 포지션 공통코드 등록
        print("포지션 공통코드 등록 중...")
        for pos in POSITIONS:
            await db.execute(text("""
                INSERT INTO common_cd_b (group_cd, code, code_name, code_seq, use_yn, create_id, create_dt, update_id, update_dt)
                VALUES (:group_cd, :code, :code_name, :seq, 'Y', 'system', :now, 'system', :now)
                ON CONFLICT (group_cd, code) DO UPDATE SET code_name = EXCLUDED.code_name, use_yn = 'Y', update_dt = :now
            """), {'group_cd': 'position_cd', 'code': pos['code'], 'code_name': pos['code_name'], 'seq': pos['seq'], 'now': now})
        await db.commit()

        # 2. 포지션 가중치 등록
        print("포지션 가중치 등록 중...")
        for position_cd, weights in WEIGHTS.items():
            total = sum(weights.values())
            print(f"  {position_cd}: {len(weights)}개 스탯, 총합={total:.3f}")
            for score_cd, val in weights.items():
                await db.execute(text("""
                    INSERT INTO position_point_b (position_cd, score_cd, position_val, create_id, create_dt, update_id, update_dt)
                    VALUES (:pos_cd, :sc_cd, :val, 'system', :now, 'system', :now)
                    ON CONFLICT (position_cd, score_cd) DO UPDATE SET position_val = EXCLUDED.position_val, update_dt = :now
                """), {'pos_cd': position_cd, 'sc_cd': score_cd, 'val': val, 'now': now})
        
        await db.commit()
        print("✅ 데이터 등록 완료!")

if __name__ == "__main__":
    asyncio.run(seed())
