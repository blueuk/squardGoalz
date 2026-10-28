from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from database import get_db
from models.UserB import UserB
from payment.paymentRequest import *
from payment.paymentResponse import *
from payment import paymentService

router = APIRouter(prefix='/payment', tags=['Payment'])

def get_session_userid(request: Request) -> str:
    userid = request.session.get("userid")
    if not userid:
        raise HTTPException(status_code=401, detail="로그인이 필요합니다.")
    return userid

async def get_admin_userid(request: Request, db: AsyncSession) -> str:
    userid = get_session_userid(request)
    result = await db.execute(select(UserB.auth_cd).where(UserB.userid == userid))
    if result.scalar() != "01":  # 01: 관리자
        raise HTTPException(status_code=403, detail="관리자만 수정할 수 있습니다.")
    return userid

@router.get('/search', response_model=List[PaymentResponse])
async def search(req: PaymentSearchRequest = Depends(), db: AsyncSession = Depends(get_db)):
    return await paymentService.get(db, req)

@router.post('/insert', response_model=MessageResponse)
async def insert(req: PaymentInsertRequest, request: Request, db: AsyncSession = Depends(get_db)):
    await paymentService.insert(db, req, await get_admin_userid(request, db))
    return MessageResponse(message='Insert Success')

@router.post('/update', response_model=MessageResponse)
async def update(req: PaymentUpdateRequest, request: Request, db: AsyncSession = Depends(get_db)):
    try:
        await paymentService.update(db, req, await get_admin_userid(request, db))
        return MessageResponse(message='Update Success')
    except ValueError:
        raise HTTPException(404, 'Not found')

@router.post('/delete', response_model=MessageResponse)
async def delete(req: PaymentDeleteRequest, request: Request, db: AsyncSession = Depends(get_db)):
    await get_admin_userid(request, db)
    await paymentService.delete_obj(db, req)
    return MessageResponse(message='Delete Success')

