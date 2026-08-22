from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from datetime import datetime
from models.TeamMemberScoreL import TeamMemberScoreL
from memberScore import memberScoreRequest

async def get(db: AsyncSession, req: memberScoreRequest.MemberscoreSearchRequest):
    query = select(TeamMemberScoreL)
    if req.member_uid is not None:
        query = query.filter(TeamMemberScoreL.member_uid == req.member_uid)
    if req.team_uid is not None:
        query = query.filter(TeamMemberScoreL.team_uid == req.team_uid)
    if req.year is not None:
        query = query.filter(TeamMemberScoreL.year == req.year)
    if req.score_cd is not None:
        query = query.filter(TeamMemberScoreL.score_cd == req.score_cd)
    result = await db.execute(query)
    return result.scalars().all()

async def insert(db: AsyncSession, req: memberScoreRequest.MemberscoreInsertRequest, session_id: str):
    now = datetime.now()
    obj = TeamMemberScoreL(
        member_uid=req.member_uid,
        team_uid=req.team_uid,
        year=req.year,
        score_cd=req.score_cd,
        score_val=req.score_val,
        create_id=session_id,
        create_dt=now,
        update_id=session_id,
        update_dt=now,
    )
    db.add(obj)
    await db.commit()
    return obj

async def update(db: AsyncSession, req: memberScoreRequest.MemberscoreUpdateRequest, session_id: str):
    query = select(TeamMemberScoreL)
    query = query.filter(TeamMemberScoreL.member_uid == req.member_uid)
    query = query.filter(TeamMemberScoreL.team_uid == req.team_uid)
    query = query.filter(TeamMemberScoreL.year == req.year)
    query = query.filter(TeamMemberScoreL.score_cd == req.score_cd)
    result = await db.execute(query)
    obj = result.scalars().first()
    if not obj: raise ValueError('Not found')
    if req.score_val is not None: obj.score_val = req.score_val
    if hasattr(obj, 'update_id'): obj.update_id = session_id
    if hasattr(obj, 'update_dt'): obj.update_dt = datetime.now()
    await db.commit()
    return obj

async def delete_obj(db: AsyncSession, req: memberScoreRequest.MemberscoreDeleteRequest):
    query = delete(TeamMemberScoreL)
    query = query.where(TeamMemberScoreL.member_uid == req.member_uid)
    query = query.where(TeamMemberScoreL.team_uid == req.team_uid)
    query = query.where(TeamMemberScoreL.year == req.year)
    query = query.where(TeamMemberScoreL.score_cd == req.score_cd)
    await db.execute(query)
    await db.commit()
