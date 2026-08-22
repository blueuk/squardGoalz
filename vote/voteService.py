from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from datetime import datetime
from models.TeamVoteL import TeamVoteL
from vote import voteRequest

async def get(db: AsyncSession, req: voteRequest.VoteSearchRequest):
    query = select(TeamVoteL)
    if req.vote_seq is not None:
        query = query.filter(TeamVoteL.vote_seq == req.vote_seq)
    if req.team_uid is not None:
        query = query.filter(TeamVoteL.team_uid == req.team_uid)
    result = await db.execute(query)
    return result.scalars().all()

async def insert(db: AsyncSession, req: voteRequest.VoteInsertRequest, session_id: str):
    now = datetime.now()
    obj = TeamVoteL(
        vote_seq=req.vote_seq,
        team_uid=req.team_uid,
        play_date=req.play_date,
        play_start_time=req.play_start_time,
        play_end_time=req.play_end_time,
        member_uid=req.member_uid,
        vote_cd=req.vote_cd,
        create_id=session_id,
        create_dt=now,
        update_id=session_id,
        update_dt=now,
    )
    db.add(obj)
    await db.commit()
    return obj

async def update(db: AsyncSession, req: voteRequest.VoteUpdateRequest, session_id: str):
    query = select(TeamVoteL)
    query = query.filter(TeamVoteL.vote_seq == req.vote_seq)
    query = query.filter(TeamVoteL.team_uid == req.team_uid)
    result = await db.execute(query)
    obj = result.scalars().first()
    if not obj: raise ValueError('Not found')
    if req.play_date is not None: obj.play_date = req.play_date
    if req.play_start_time is not None: obj.play_start_time = req.play_start_time
    if req.play_end_time is not None: obj.play_end_time = req.play_end_time
    if req.member_uid is not None: obj.member_uid = req.member_uid
    if req.vote_cd is not None: obj.vote_cd = req.vote_cd
    if hasattr(obj, 'update_id'): obj.update_id = session_id
    if hasattr(obj, 'update_dt'): obj.update_dt = datetime.now()
    await db.commit()
    return obj

async def delete_obj(db: AsyncSession, req: voteRequest.VoteDeleteRequest):
    query = delete(TeamVoteL)
    query = query.where(TeamVoteL.vote_seq == req.vote_seq)
    query = query.where(TeamVoteL.team_uid == req.team_uid)
    await db.execute(query)
    await db.commit()
