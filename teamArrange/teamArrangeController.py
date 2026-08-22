from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from database import get_db
from teamArrange.teamArrangeRequest import *
from teamArrange.teamArrangeResponse import *
from teamArrange import teamArrangeService

router = APIRouter(prefix='/teamArrange', tags=['Teamarrange'])

def get_session_userid(request: Request) -> str:
    return request.session.get('userid', 'test_user')

@router.get('/search', response_model=List[TeamarrangeResponse])
async def search(req: TeamarrangeSearchRequest = Depends(), db: AsyncSession = Depends(get_db)):
    return await teamArrangeService.get(db, req)

@router.post('/insert', response_model=MessageResponse)
async def insert(req: TeamarrangeInsertRequest, request: Request, db: AsyncSession = Depends(get_db)):
    await teamArrangeService.insert(db, req, get_session_userid(request))
    return MessageResponse(message='Insert Success')

@router.post('/update', response_model=MessageResponse)
async def update(req: TeamarrangeUpdateRequest, request: Request, db: AsyncSession = Depends(get_db)):
    try:
        await teamArrangeService.update(db, req, get_session_userid(request))
        return MessageResponse(message='Update Success')
    except ValueError:
        raise HTTPException(404, 'Not found')

@router.post('/delete', response_model=MessageResponse)
async def delete(req: TeamarrangeDeleteRequest, request: Request, db: AsyncSession = Depends(get_db)):
    await teamArrangeService.delete_obj(db, req)
    return MessageResponse(message='Delete Success')

