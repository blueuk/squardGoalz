from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from datetime import datetime
from models.TeamScheduleL import TeamScheduleL
from models.TeamMemberL import TeamMemberL
from models.TeamVoteL import TeamVoteL
from schedule import scheduleRequest

async def get(db: AsyncSession, req: scheduleRequest.ScheduleSearchRequest):
    query = select(TeamScheduleL)
    if req.vote_seq is not None:
        query = query.filter(TeamScheduleL.vote_seq == req.vote_seq)
    if req.team_uid is not None:
        query = query.filter(TeamScheduleL.team_uid == req.team_uid)
    result = await db.execute(query)
    return result.scalars().all()

async def insert(db: AsyncSession, req: scheduleRequest.ScheduleInsertRequest, session_id: str):
    now = datetime.now()
    obj = TeamScheduleL(
        team_uid=req.team_uid,
        play_date=req.play_date,
        play_start_time=req.play_start_time,
        play_end_time=req.play_end_time,
        play_location=req.play_location,
        vote_period_from=req.vote_period_from,
        vote_period_to=req.vote_period_to,
        vote_end_yn=req.vote_end_yn,
        create_id=session_id,
        create_dt=now,
        update_id=session_id,
        update_dt=now,
    )
    db.add(obj)
    await db.flush() # vote_seq를 먼저 할당받기 위함

    # 2. 모든 멤버 조회
    member_query = select(TeamMemberL).filter(TeamMemberL.team_uid == req.team_uid)
    members_result = await db.execute(member_query)
    members = members_result.scalars().all()

    # 3. 모든 멤버를 미투표(01) 상태로 vote 추가
    for member in members:
        vote_obj = TeamVoteL(
            vote_seq=obj.vote_seq,
            team_uid=req.team_uid,
            play_date=req.play_date,
            play_start_time=req.play_start_time,
            play_end_time=req.play_end_time,
            member_uid=member.member_uid,
            vote_cd='01', # 01: 미투표, 02: 참석, 03: 불참
            create_id=session_id,
            create_dt=now,
            update_id=session_id,
            update_dt=now
        )
        db.add(vote_obj)

    await db.commit()
    return obj

async def update(db: AsyncSession, req: scheduleRequest.ScheduleUpdateRequest, session_id: str):
    query = select(TeamScheduleL)
    query = query.filter(TeamScheduleL.vote_seq == req.vote_seq)
    query = query.filter(TeamScheduleL.team_uid == req.team_uid)
    result = await db.execute(query)
    obj = result.scalars().first()
    if not obj: raise ValueError('Not found')
    if req.play_date is not None: obj.play_date = req.play_date
    if req.play_start_time is not None: obj.play_start_time = req.play_start_time
    if req.play_end_time is not None: obj.play_end_time = req.play_end_time
    if req.play_location is not None: obj.play_location = req.play_location
    if req.vote_period_from is not None: obj.vote_period_from = req.vote_period_from
    if req.vote_period_to is not None: obj.vote_period_to = req.vote_period_to
    if req.vote_end_yn is not None: obj.vote_end_yn = req.vote_end_yn
    if hasattr(obj, 'update_id'): obj.update_id = session_id
    if hasattr(obj, 'update_dt'): obj.update_dt = datetime.now()
    await db.commit()
    return obj

async def delete_obj(db: AsyncSession, req: scheduleRequest.ScheduleDeleteRequest):
    query = delete(TeamScheduleL)
    query = query.where(TeamScheduleL.vote_seq == req.vote_seq)
    query = query.where(TeamScheduleL.team_uid == req.team_uid)
    await db.execute(query)
    await db.commit()
