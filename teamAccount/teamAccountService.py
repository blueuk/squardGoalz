from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update as sql_update
from datetime import datetime
from models.TeamAccountL import TeamAccountL
from teamAccount import teamAccountRequest

async def get(db: AsyncSession, req: teamAccountRequest.TeamaccountSearchRequest):
    query = select(TeamAccountL)
    if req.team_uid is not None:
        query = query.filter(TeamAccountL.team_uid == req.team_uid)
    if req.team_account_seq is not None:
        query = query.filter(TeamAccountL.team_account_seq == req.team_account_seq)
    if req.bank_cd is not None:
        query = query.filter(TeamAccountL.bank_cd == req.bank_cd)
    if req.account_enc is not None:
        query = query.filter(TeamAccountL.account_enc == req.account_enc)
    result = await db.execute(query)
    return result.scalars().all()

async def insert(db: AsyncSession, req: teamAccountRequest.TeamaccountInsertRequest, session_id: str):
    now = datetime.now()
    obj = TeamAccountL(
        team_uid=req.team_uid,
        bank_cd=req.bank_cd,
        account_enc=req.account_enc,
        create_id=session_id,
        create_dt=now,
        update_id=session_id,
        update_dt=now,
    )
    db.add(obj)
    await db.commit()
    return obj

async def update(db: AsyncSession, req: teamAccountRequest.TeamaccountUpdateRequest, session_id: str):
    stmt = sql_update(TeamAccountL).where(
        TeamAccountL.team_uid == req.team_uid,
        TeamAccountL.team_account_seq == req.team_account_seq
    ).values(
        bank_cd=req.bank_cd,
        account_enc=req.account_enc,
        update_id=session_id,
        update_dt=datetime.now()
    )
    res = await db.execute(stmt)
    if res.rowcount == 0:
        raise ValueError('Not found')
    await db.commit()
    return True

async def delete_obj(db: AsyncSession, req: teamAccountRequest.TeamaccountDeleteRequest):
    query = delete(TeamAccountL)
    query = query.where(TeamAccountL.team_uid == req.team_uid)
    query = query.where(TeamAccountL.team_account_seq == req.team_account_seq)
    query = query.where(TeamAccountL.bank_cd == req.bank_cd)
    query = query.where(TeamAccountL.account_enc == req.account_enc)
    await db.execute(query)
    await db.commit()
