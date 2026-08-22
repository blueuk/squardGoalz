from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from datetime import datetime
from models.TeamRecordL import TeamRecordL
from record import recordRequest

async def get(db: AsyncSession, req: recordRequest.RecordSearchRequest):
    query = select(TeamRecordL)
    if req.team_uid is not None:
        query = query.filter(TeamRecordL.team_uid == req.team_uid)
    if req.vote_uid is not None:
        query = query.filter(TeamRecordL.vote_uid == req.vote_uid)
    if req.play_date is not None:
        query = query.filter(TeamRecordL.play_date == req.play_date)
    result = await db.execute(query)
    return result.scalars().all()

async def insert(db: AsyncSession, req: recordRequest.RecordInsertRequest, session_id: str):
    now = datetime.now()
    obj = TeamRecordL(
        team_uid=req.team_uid,
        vote_uid=req.vote_uid,
        play_date=req.play_date,
        member_uid=req.member_uid,
        goal_cnt=req.goal_cnt,
        asist_cnt=req.asist_cnt,
        create_id=session_id,
        create_dt=now,
        update_id=session_id,
        update_dt=now,
    )
    db.add(obj)
    await db.commit()
    return obj

async def update(db: AsyncSession, req: recordRequest.RecordUpdateRequest, session_id: str):
    query = select(TeamRecordL)
    query = query.filter(TeamRecordL.team_uid == req.team_uid)
    query = query.filter(TeamRecordL.vote_uid == req.vote_uid)
    query = query.filter(TeamRecordL.play_date == req.play_date)
    result = await db.execute(query)
    obj = result.scalars().first()
    if not obj: raise ValueError('Not found')
    if req.member_uid is not None: obj.member_uid = req.member_uid
    if req.goal_cnt is not None: obj.goal_cnt = req.goal_cnt
    if req.asist_cnt is not None: obj.asist_cnt = req.asist_cnt
    if hasattr(obj, 'update_id'): obj.update_id = session_id
    if hasattr(obj, 'update_dt'): obj.update_dt = datetime.now()
    await db.commit()
    return obj

async def delete_obj(db: AsyncSession, req: recordRequest.RecordDeleteRequest):
    query = delete(TeamRecordL)
    query = query.where(TeamRecordL.team_uid == req.team_uid)
    query = query.where(TeamRecordL.vote_uid == req.vote_uid)
    query = query.where(TeamRecordL.play_date == req.play_date)
    await db.execute(query)
    await db.commit()
