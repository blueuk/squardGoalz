from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from database import get_db
from payment.paymentRequest import *
from payment.paymentResponse import *
from payment import paymentService

router = APIRouter(prefix='/payment', tags=['Payment'])

def get_session_userid(request: Request) -> str:
    return request.session.get('userid', 'test_user')

@router.get('/search', response_model=List[PaymentResponse])
async def search(req: PaymentSearchRequest = Depends(), db: AsyncSession = Depends(get_db)):
    return await paymentService.get(db, req)

@router.post('/insert', response_model=MessageResponse)
async def insert(req: PaymentInsertRequest, request: Request, db: AsyncSession = Depends(get_db)):
    await paymentService.insert(db, req, get_session_userid(request))
    return MessageResponse(message='Insert Success')

@router.post('/update', response_model=MessageResponse)
async def update(req: PaymentUpdateRequest, request: Request, db: AsyncSession = Depends(get_db)):
    try:
        await paymentService.update(db, req, get_session_userid(request))
        return MessageResponse(message='Update Success')
    except ValueError:
        raise HTTPException(404, 'Not found')

@router.post('/delete', response_model=MessageResponse)
async def delete(req: PaymentDeleteRequest, request: Request, db: AsyncSession = Depends(get_db)):
    await paymentService.delete_obj(db, req)
    return MessageResponse(message='Delete Success')

