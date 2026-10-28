from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.dialects.postgresql import insert as pg_insert
from datetime import datetime
from models.PositionPointB import PositionPointB
from models.CommonCdB import CommonCdB
from models.TeamMemberL import TeamMemberL
from models.TeamMemberScoreL import TeamMemberScoreL
from position_point import positionRequest

async def check_common_code(db: AsyncSession, group_cd: str, code: str) -> bool:
    result = await db.execute(select(CommonCdB).filter(CommonCdB.group_cd == group_cd, CommonCdB.code == code))
    return result.scalars().first() is not None

async def get_position_points(db: AsyncSession, req: positionRequest.PositionPointSearchRequest):
    query = select(PositionPointB)
    if req.position_cd:
        query = query.filter(PositionPointB.position_cd == req.position_cd)
    if req.score_cd:
        query = query.filter(PositionPointB.score_cd == req.score_cd)
    result = await db.execute(query)
    return result.scalars().all()

async def insert_position_point(db: AsyncSession, req: positionRequest.PositionPointInsertRequest, session_id: str):
    is_valid_position = await check_common_code(db, "position_cd", req.position_cd)
    if not is_valid_position:
        raise ValueError(f"유효하지 않은 position_cd 입니다. (공통코드에 존재하지 않음)")
    is_valid_score = await check_common_code(db, "score_cd", req.score_cd)
    if not is_valid_score:
        raise ValueError(f"유효하지 않은 score_cd 입니다. (공통코드에 존재하지 않음)")
    now = datetime.now()
    obj = PositionPointB(
        position_cd=req.position_cd,
        score_cd=req.score_cd,
        position_val=req.position_val,
        create_id=session_id,
        create_dt=now,
        update_id=session_id,
        update_dt=now
    )
    db.add(obj)
    await db.commit()
    return obj

async def upsert_position_point(db: AsyncSession, req: positionRequest.PositionPointUpdateRequest, session_id: str):
    """position_cd + score_cd 복합키로 upsert (없으면 insert, 있으면 update)"""
    result = await db.execute(
        select(PositionPointB).filter(
            PositionPointB.position_cd == req.position_cd,
            PositionPointB.score_cd == req.score_cd
        )
    )
    obj = result.scalars().first()
    now = datetime.now()
    if obj:
        obj.position_val = req.position_val
        obj.update_id = session_id
        obj.update_dt = now
    else:
        obj = PositionPointB(
            position_cd=req.position_cd,
            score_cd=req.score_cd,
            position_val=req.position_val,
            create_id=session_id,
            create_dt=now,
            update_id=session_id,
            update_dt=now
        )
        db.add(obj)
    await db.commit()
    return obj

async def bulk_upsert_position_points(db: AsyncSession, items: list, session_id: str):
    """여러 가중치를 한 번의 INSERT ... ON CONFLICT 문과 한 번의 commit으로 저장합니다."""
    if not items:
        return
    now = datetime.now()
    stmt = pg_insert(PositionPointB).values([
        {
            "position_cd": item.position_cd,
            "score_cd": item.score_cd,
            "position_val": item.position_val,
            "create_id": session_id,
            "create_dt": now,
            "update_id": session_id,
            "update_dt": now,
        }
        for item in items
    ])
    stmt = stmt.on_conflict_do_update(
        index_elements=[PositionPointB.position_cd, PositionPointB.score_cd],
        set_={
            "position_val": stmt.excluded.position_val,
            "update_id": stmt.excluded.update_id,
            "update_dt": stmt.excluded.update_dt,
        }
    )
    await db.execute(stmt)
    await db.commit()

async def update_position_point(db: AsyncSession, req: positionRequest.PositionPointUpdateRequest, session_id: str):
    result = await db.execute(
        select(PositionPointB).filter(
            PositionPointB.position_cd == req.position_cd,
            PositionPointB.score_cd == req.score_cd
        )
    )
    obj = result.scalars().first()
    if not obj:
        raise ValueError("업데이트할 데이터가 존재하지 않습니다.")
    obj.position_val = req.position_val
    obj.update_id = session_id
    obj.update_dt = datetime.now()
    await db.commit()
    return obj

async def delete_position_point(db: AsyncSession, req: positionRequest.PositionPointDeleteRequest):
    result = await db.execute(
        select(PositionPointB).filter(
            PositionPointB.position_cd == req.position_cd,
            PositionPointB.score_cd == req.score_cd
        )
    )
    obj = result.scalars().first()
    if not obj:
        raise ValueError("삭제할 데이터가 존재하지 않습니다.")
    await db.execute(
        delete(PositionPointB).where(
            PositionPointB.position_cd == req.position_cd,
            PositionPointB.score_cd == req.score_cd
        )
    )
    await db.commit()

# ================== 능력치(가중치) 항목 추가 / 삭제 ==================
DEFAULT_NEW_SCORE_VAL = 10
SCORE_YEAR = '2026'  # teamMemberService.insert_team_members 와 동일한 기준 년도

async def insert_score_item(db: AsyncSession, req: positionRequest.ScoreItemInsertRequest, session_id: str):
    code_name = req.code_name.strip()
    if not code_name:
        raise ValueError("항목 이름을 입력해주세요.")

    score_cds = (await db.execute(select(CommonCdB).where(CommonCdB.group_cd == 'score_cd'))).scalars().all()
    if any(c.code_name == code_name for c in score_cds):
        raise ValueError(f"이미 존재하는 항목입니다: {code_name}")

    next_num = max((int(c.code) for c in score_cds if c.code.isdigit()), default=0) + 1
    new_code = f"{next_num:03d}"
    next_seq = max((c.code_seq or 0 for c in score_cds), default=0) + 1
    now = datetime.now()

    # 1. 공통코드 등록
    db.add(CommonCdB(
        group_cd='score_cd', code=new_code, code_name=code_name, code_seq=next_seq,
        reference_2=req.category, use_yn='Y',
        create_id=session_id, create_dt=now, update_id=session_id, update_dt=now
    ))

    # 2. 모든 포지션에 가중치 0으로 추가 (포지션별 총합 1.0 유지)
    position_cds = (await db.execute(select(PositionPointB.position_cd).distinct())).scalars().all()
    for position_cd in position_cds:
        db.add(PositionPointB(
            position_cd=position_cd, score_cd=new_code, position_val=0,
            create_id=session_id, create_dt=now, update_id=session_id, update_dt=now
        ))

    # 3. 선수단 전원에게 기본점수 부여
    members = (await db.execute(select(TeamMemberL.team_uid, TeamMemberL.member_uid))).all()
    for team_uid, member_uid in members:
        db.add(TeamMemberScoreL(
            member_uid=member_uid, team_uid=team_uid, year=SCORE_YEAR,
            score_cd=new_code, score_val=DEFAULT_NEW_SCORE_VAL,
            create_id=session_id, create_dt=now, update_id=session_id, update_dt=now
        ))

    await db.commit()
    return {
        "score_cd": new_code, "code_name": code_name, "code_seq": next_seq,
        "category": req.category, "member_count": len(members)
    }

async def delete_score_item(db: AsyncSession, req: positionRequest.ScoreItemDeleteRequest):
    result = await db.execute(
        select(CommonCdB).where(CommonCdB.group_cd == 'score_cd', CommonCdB.code == req.score_cd)
    )
    if not result.scalars().first():
        raise ValueError("삭제할 항목이 존재하지 않습니다.")

    # 항목에 연결된 가중치 / 선수 점수 / 공통코드를 함께 삭제합니다.
    await db.execute(delete(PositionPointB).where(PositionPointB.score_cd == req.score_cd))
    await db.execute(delete(TeamMemberScoreL).where(TeamMemberScoreL.score_cd == req.score_cd))
    await db.execute(delete(CommonCdB).where(CommonCdB.group_cd == 'score_cd', CommonCdB.code == req.score_cd))
    await db.commit()
