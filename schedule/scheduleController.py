from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from database import get_db
from schedule.scheduleRequest import *
from schedule.scheduleResponse import *
from schedule import scheduleService

router = APIRouter(prefix='/schedule', tags=['Schedule'])

def get_session_userid(request: Request) -> str:
    return request.session.get('userid', 'test_user')

@router.get('/search', response_model=List[ScheduleResponse])
async def search(req: ScheduleSearchRequest = Depends(), db: AsyncSession = Depends(get_db)):
    return await scheduleService.get(db, req)

@router.post('/insert', response_model=MessageResponse)
async def insert(req: ScheduleInsertRequest, request: Request, db: AsyncSession = Depends(get_db)):
    await scheduleService.insert(db, req, get_session_userid(request))
    return MessageResponse(message='Insert Success')

@router.post('/update', response_model=MessageResponse)
async def update(req: ScheduleUpdateRequest, request: Request, db: AsyncSession = Depends(get_db)):
    try:
        await scheduleService.update(db, req, get_session_userid(request))
        return MessageResponse(message='Update Success')
    except ValueError:
        raise HTTPException(404, 'Not found')

@router.post('/delete', response_model=MessageResponse)
async def delete(req: ScheduleDeleteRequest, request: Request, db: AsyncSession = Depends(get_db)):
    await scheduleService.delete_obj(db, req)
    return MessageResponse(message='Delete Success')

