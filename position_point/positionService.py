from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from datetime import datetime
from models.PositionPointB import PositionPointB
from models.CommonCdB import CommonCdB
from position_point import positionRequest

async def check_common_code(db: AsyncSession, group_cd: str, code: str) -> bool:
    """공통코드(common_cd_b)에 그룹코드와 코드가 매칭되는지 확인"""
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
    # 공통코드 무결성 검증 (요청사항: position_cd, score_cd가 공통코드에 있어야 함)
    # 문맥에 따라 각각의 그룹코드('position_cd', 'score_cd') 내에 존재하는지 검증하도록 했습니다.
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

