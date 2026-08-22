from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from datetime import datetime
from models.TeamStartdiumL import TeamStartdiumL
from stardium import stardiumRequest

async def get(db: AsyncSession, req: stardiumRequest.StardiumSearchRequest):
    query = select(TeamStartdiumL)
    if req.team_uid is not None:
        query = query.filter(TeamStartdiumL.team_uid == req.team_uid)
    if req.team_stardium_seq is not None:
        query = query.filter(TeamStartdiumL.team_stardium_seq == req.team_stardium_seq)
    result = await db.execute(query)
    return result.scalars().all()

async def insert(db: AsyncSession, req: stardiumRequest.StardiumInsertRequest, session_id: str):
    now = datetime.now()
    obj = TeamStartdiumL(
        team_uid=req.team_uid,
        location=req.location,
        start_time=req.start_time,
        end_time=req.end_time,
        day_cd=req.day_cd,
        main_locate_yn=req.main_locate_yn,
        create_id=session_id,
        create_dt=now,
        update_id=session_id,
        update_dt=now,
    )
    db.add(obj)
    await db.commit()
    return obj

async def update(db: AsyncSession, req: stardiumRequest.StardiumUpdateRequest, session_id: str):
    query = select(TeamStartdiumL)
    query = query.filter(TeamStartdiumL.team_uid == req.team_uid)
    query = query.filter(TeamStartdiumL.team_stardium_seq == req.team_stardium_seq)
    result = await db.execute(query)
    obj = result.scalars().first()
    if not obj: raise ValueError('Not found')
    if req.location is not None: obj.location = req.location
    if req.start_time is not None: obj.start_time = req.start_time
    if req.end_time is not None: obj.end_time = req.end_time
    if req.day_cd is not None: obj.day_cd = req.day_cd
    if req.main_locate_yn is not None: obj.main_locate_yn = req.main_locate_yn
    if hasattr(obj, 'update_id'): obj.update_id = session_id
    if hasattr(obj, 'update_dt'): obj.update_dt = datetime.now()
    await db.commit()
    return obj

async def delete_obj(db: AsyncSession, req: stardiumRequest.StardiumDeleteRequest):
    query = delete(TeamStartdiumL)
    query = query.where(TeamStartdiumL.team_uid == req.team_uid)
    query = query.where(TeamStartdiumL.team_stardium_seq == req.team_stardium_seq)
    await db.execute(query)
    await db.commit()
