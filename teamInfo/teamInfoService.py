from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from datetime import datetime
import uuid
from models.TeamInfoB import TeamInfoB
from models.CommonCdB import CommonCdB
from teamInfo import teamInfoRequest

async def check_common_code(db: AsyncSession, group_cd: str, code: str) -> bool:
    """공통코드(common_cd_b)에 존재하는지 확인"""
    if not code:
        return True
    result = await db.execute(select(CommonCdB).filter(CommonCdB.group_cd == group_cd, CommonCdB.code == code))
    return result.scalars().first() is not None

async def validate_common_codes(db: AsyncSession, req):
    """요청의 공통코드 필드들 유효성 검사"""
    if hasattr(req, 'region_cd') and req.region_cd:
        if not await check_common_code(db, "region_cd", req.region_cd):
            raise ValueError("유효하지 않은 region_cd 입니다. (공통코드 누락)")
    if hasattr(req, 'day_cd') and req.day_cd:
        if not await check_common_code(db, "day_cd", req.day_cd):
            raise ValueError("유효하지 않은 day_cd 입니다. (공통코드 누락)")
    if hasattr(req, 'level_cd') and req.level_cd:
        if not await check_common_code(db, "level_cd", req.level_cd):
            raise ValueError("유효하지 않은 level_cd 입니다. (공통코드 누락)")
    if hasattr(req, 'gender_cd') and req.gender_cd:
        if not await check_common_code(db, "gender_cd", req.gender_cd):
            raise ValueError("유효하지 않은 gender_cd 입니다. (공통코드 누락)")

async def get_team_info(db: AsyncSession, req: teamInfoRequest.TeamInfoSearchRequest):
    query = select(TeamInfoB)
    if req.team_uid:
        query = query.filter(TeamInfoB.team_uid == req.team_uid)
    if req.teamname:
        query = query.filter(TeamInfoB.teamname.like(f"%{req.teamname}%"))
    if req.region_cd:
        query = query.filter(TeamInfoB.region_cd == req.region_cd)
    if req.day_cd:
        query = query.filter(TeamInfoB.day_cd == req.day_cd)
    if req.level_cd:
        query = query.filter(TeamInfoB.level_cd == req.level_cd)
    if req.gender_cd:
        query = query.filter(TeamInfoB.gender_cd == req.gender_cd)
    if req.use_yn:
        query = query.filter(TeamInfoB.use_yn == req.use_yn)
        
    result = await db.execute(query)
    return result.scalars().all()

async def insert_team_info(db: AsyncSession, req: teamInfoRequest.TeamInfoInsertRequest, session_id: str):
    await validate_common_codes(db, req)
        
    now = datetime.now()
    # 겹치지 않는 고유 고유 식별자(UUID) 생성
    new_team_uid = str(uuid.uuid4())
    
    obj = TeamInfoB(
        team_uid=new_team_uid,
        teamname=req.teamname,
        region_cd=req.region_cd,
        location=req.location,
        start_time=req.start_time,
        end_time=req.end_time,
        day_cd=req.day_cd,
        level_cd=req.level_cd,
        gender_cd=req.gender_cd,
        use_yn=req.use_yn,
        comment=req.comment,
        create_id=session_id,
        create_dt=now,
        update_id=session_id,
        update_dt=now
    )
    db.add(obj)
    await db.commit()
    return obj

async def update_team_info(db: AsyncSession, req: teamInfoRequest.TeamInfoUpdateRequest, session_id: str):
    await validate_common_codes(db, req)
    
    result = await db.execute(select(TeamInfoB).filter(TeamInfoB.team_uid == req.team_uid))
    obj = result.scalars().first()
    
    if not obj:
        raise ValueError("업데이트할 팀이 존재하지 않습니다.")
        
    if req.teamname is not None: obj.teamname = req.teamname
    if req.region_cd is not None: obj.region_cd = req.region_cd
    if req.location is not None: obj.location = req.location
    if req.start_time is not None: obj.start_time = req.start_time
    if req.end_time is not None: obj.end_time = req.end_time
    if req.day_cd is not None: obj.day_cd = req.day_cd
    if req.level_cd is not None: obj.level_cd = req.level_cd
    if req.gender_cd is not None: obj.gender_cd = req.gender_cd
    if req.use_yn is not None: obj.use_yn = req.use_yn
    if req.comment is not None: obj.comment = req.comment
    
    obj.update_id = session_id
    obj.update_dt = datetime.now()
    
    await db.commit()
    return obj

async def delete_team_info(db: AsyncSession, req: teamInfoRequest.TeamInfoDeleteRequest):
    result = await db.execute(select(TeamInfoB).filter(TeamInfoB.team_uid == req.team_uid))
    obj = result.scalars().first()
    
    if not obj:
        raise ValueError("삭제할 팀이 존재하지 않습니다.")
        
    await db.execute(delete(TeamInfoB).where(TeamInfoB.team_uid == req.team_uid))
    await db.commit()

