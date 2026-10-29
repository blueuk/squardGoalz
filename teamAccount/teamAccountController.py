from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from database import get_db
from auth import require_permission
from teamAccount.teamAccountRequest import *
from teamAccount.teamAccountResponse import *
from teamAccount import teamAccountService

router = APIRouter(prefix='/teamAccount', tags=['Teamaccount'])

@router.get('/search', response_model=List[TeamaccountResponse])
async def search(req: TeamaccountSearchRequest = Depends(), db: AsyncSession = Depends(get_db)):
    return await teamAccountService.get(db, req)

@router.post('/insert', response_model=MessageResponse)
async def insert(req: TeamaccountInsertRequest, request: Request, db: AsyncSession = Depends(get_db)):
    userid = await require_permission(request, db, 'payment.edit')
    await teamAccountService.insert(db, req, userid)
    return MessageResponse(message='Insert Success')

@router.post('/update', response_model=MessageResponse)
async def update(req: TeamaccountUpdateRequest, request: Request, db: AsyncSession = Depends(get_db)):
    try:
        userid = await require_permission(request, db, 'payment.edit')
        await teamAccountService.update(db, req, userid)
        return MessageResponse(message='Update Success')
    except ValueError:
        raise HTTPException(404, 'Not found')

@router.post('/delete', response_model=MessageResponse)
async def delete(req: TeamaccountDeleteRequest, request: Request, db: AsyncSession = Depends(get_db)):
    await require_permission(request, db, 'payment.edit')
    await teamAccountService.delete_obj(db, req)
    return MessageResponse(message='Delete Success')

