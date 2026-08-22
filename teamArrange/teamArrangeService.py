from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from datetime import datetime
from models.TeamArrangeL import TeamArrangeL
from teamArrange import teamArrangeRequest

async def get(db: AsyncSession, req: teamArrangeRequest.TeamarrangeSearchRequest):
    query = select(TeamArrangeL)
    if req.vote_uid is not None:
        query = query.filter(TeamArrangeL.vote_uid == req.vote_uid)
    result = await db.execute(query)
    return result.scalars().all()

async def insert(db: AsyncSession, req: teamArrangeRequest.TeamarrangeInsertRequest, session_id: str):
    now = datetime.now()
    obj = TeamArrangeL(
        vote_uid=req.vote_uid,
        play_date=req.play_date,
        team_cd=req.team_cd,
        member_id=req.member_id,
        create_id=session_id,
        create_dt=now,
        update_id=session_id,
        update_dt=now,
    )
    db.add(obj)
    await db.commit()
    return obj

async def update(db: AsyncSession, req: teamArrangeRequest.TeamarrangeUpdateRequest, session_id: str):
    query = select(TeamArrangeL)
    query = query.filter(TeamArrangeL.vote_uid == req.vote_uid)
    result = await db.execute(query)
    obj = result.scalars().first()
    if not obj: raise ValueError('Not found')
    if req.play_date is not None: obj.play_date = req.play_date
    if req.team_cd is not None: obj.team_cd = req.team_cd
    if req.member_id is not None: obj.member_id = req.member_id
    if hasattr(obj, 'update_id'): obj.update_id = session_id
    if hasattr(obj, 'update_dt'): obj.update_dt = datetime.now()
    await db.commit()
    return obj

async def delete_obj(db: AsyncSession, req: teamArrangeRequest.TeamarrangeDeleteRequest):
    query = delete(TeamArrangeL)
    query = query.where(TeamArrangeL.vote_uid == req.vote_uid)
    await db.execute(query)
    await db.commit()
