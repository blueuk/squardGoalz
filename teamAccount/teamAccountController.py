from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from database import get_db
from teamAccount.teamAccountRequest import *
from teamAccount.teamAccountResponse import *
from teamAccount import teamAccountService

router = APIRouter(prefix='/teamAccount', tags=['Teamaccount'])

def get_session_userid(request: Request) -> str:
    return request.session.get('userid', 'test_user')

@router.get('/search', response_model=List[TeamaccountResponse])
async def search(req: TeamaccountSearchRequest = Depends(), db: AsyncSession = Depends(get_db)):
    return await teamAccountService.get(db, req)

@router.post('/insert', response_model=MessageResponse)
async def insert(req: TeamaccountInsertRequest, request: Request, db: AsyncSession = Depends(get_db)):
    await teamAccountService.insert(db, req, get_session_userid(request))
    return MessageResponse(message='Insert Success')

@router.post('/update', response_model=MessageResponse)
async def update(req: TeamaccountUpdateRequest, request: Request, db: AsyncSession = Depends(get_db)):
    try:
        await teamAccountService.update(db, req, get_session_userid(request))
        return MessageResponse(message='Update Success')
    except ValueError:
        raise HTTPException(404, 'Not found')

@router.post('/delete', response_model=MessageResponse)
async def delete(req: TeamaccountDeleteRequest, request: Request, db: AsyncSession = Depends(get_db)):
    await teamAccountService.delete_obj(db, req)
    return MessageResponse(message='Delete Success')

