from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from datetime import datetime
from models.TeamArrangeL import TeamArrangeL
from models.TeamScheduleL import TeamScheduleL
from teamArrange import teamArrangeRequest

MAX_TEAM_COUNT = 4

async def get(db: AsyncSession, req: teamArrangeRequest.TeamarrangeSearchRequest):
    query = select(TeamArrangeL)
    if req.team_uid is not None:
        query = query.filter(TeamArrangeL.team_uid == req.team_uid)
    if req.vote_seq is not None:
        query = query.filter(TeamArrangeL.vote_seq == req.vote_seq)
    query = query.order_by(TeamArrangeL.team_no.asc(), TeamArrangeL.keeper_order.asc())
    result = await db.execute(query)
    return result.scalars().all()

async def save(db: AsyncSession, req: teamArrangeRequest.TeamarrangeSaveRequest, session_id: str):
    """해당 일정의 기존 배정을 지우고 새 배정으로 통째로 교체합니다."""
    schedule = (await db.execute(
        select(TeamScheduleL).filter(
            TeamScheduleL.team_uid == req.team_uid,
            TeamScheduleL.vote_seq == req.vote_seq
        )
    )).scalars().first()
    if not schedule:
        raise ValueError("배정할 일정이 존재하지 않습니다.")
    if not req.members:
        raise ValueError("배정할 인원이 없습니다.")
    if len({m.member_uid for m in req.members}) != len(req.members):
        raise ValueError("중복 배정된 인원이 있습니다.")
    if any(m.team_no < 1 or m.team_no > MAX_TEAM_COUNT for m in req.members):
        raise ValueError(f"팀 번호는 1~{MAX_TEAM_COUNT} 사이여야 합니다.")

    await db.execute(delete(TeamArrangeL).where(
        TeamArrangeL.team_uid == req.team_uid,
        TeamArrangeL.vote_seq == req.vote_seq
    ))

    now = datetime.now()
    for m in req.members:
        db.add(TeamArrangeL(
            team_uid=req.team_uid,
            vote_seq=req.vote_seq,
            member_uid=m.member_uid,
            member_name=m.member_name,
            merc_yn=m.merc_yn,
            team_no=m.team_no,
            keeper_order=m.keeper_order,
            play_date=schedule.play_date,
            create_id=session_id,
            create_dt=now,
            update_id=session_id,
            update_dt=now,
        ))
    await db.commit()

async def delete_obj(db: AsyncSession, req: teamArrangeRequest.TeamarrangeDeleteRequest):
    await db.execute(delete(TeamArrangeL).where(
        TeamArrangeL.team_uid == req.team_uid,
        TeamArrangeL.vote_seq == req.vote_seq
    ))
    await db.commit()
