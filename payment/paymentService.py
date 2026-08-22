from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from datetime import datetime
from models.TeamPaymentL import TeamPaymentL
from payment import paymentRequest

async def get(db: AsyncSession, req: paymentRequest.PaymentSearchRequest):
    query = select(TeamPaymentL)
    if req.team_uid is not None:
        query = query.filter(TeamPaymentL.team_uid == req.team_uid)
    if req.payment_cd is not None:
        query = query.filter(TeamPaymentL.payment_cd == req.payment_cd)
    if req.team_account_seq is not None:
        query = query.filter(TeamPaymentL.team_account_seq == req.team_account_seq)
    result = await db.execute(query)
    return result.scalars().all()

async def insert(db: AsyncSession, req: paymentRequest.PaymentInsertRequest, session_id: str):
    now = datetime.now()
    obj = TeamPaymentL(
        team_uid=req.team_uid,
        payment_cd=req.payment_cd,
        team_account_seq=req.team_account_seq,
        amount=req.amount,
        create_id=session_id,
        create_dt=now,
        update_id=session_id,
        update_dt=now,
    )
    db.add(obj)
    await db.commit()
    return obj

async def update(db: AsyncSession, req: paymentRequest.PaymentUpdateRequest, session_id: str):
    query = select(TeamPaymentL)
    query = query.filter(TeamPaymentL.team_uid == req.team_uid)
    query = query.filter(TeamPaymentL.payment_cd == req.payment_cd)
    query = query.filter(TeamPaymentL.team_account_seq == req.team_account_seq)
    result = await db.execute(query)
    obj = result.scalars().first()
    if not obj: raise ValueError('Not found')
    if req.amount is not None: obj.amount = req.amount
    if hasattr(obj, 'update_id'): obj.update_id = session_id
    if hasattr(obj, 'update_dt'): obj.update_dt = datetime.now()
    await db.commit()
    return obj

async def delete_obj(db: AsyncSession, req: paymentRequest.PaymentDeleteRequest):
    query = delete(TeamPaymentL)
    query = query.where(TeamPaymentL.team_uid == req.team_uid)
    query = query.where(TeamPaymentL.payment_cd == req.payment_cd)
    query = query.where(TeamPaymentL.team_account_seq == req.team_account_seq)
    await db.execute(query)
    await db.commit()
