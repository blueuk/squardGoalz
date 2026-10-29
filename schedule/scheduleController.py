from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from database import get_db
from auth import require_permission
from schedule.scheduleRequest import *
from schedule.scheduleResponse import *
from schedule import scheduleService

router = APIRouter(prefix='/schedule', tags=['Schedule'])

@router.get('/search', response_model=List[ScheduleResponse])
async def search(req: ScheduleSearchRequest = Depends(), db: AsyncSession = Depends(get_db)):
    return await scheduleService.get(db, req)

@router.post('/insert', response_model=MessageResponse)
async def insert(req: ScheduleInsertRequest, request: Request, db: AsyncSession = Depends(get_db)):
    userid = await require_permission(request, db, 'schedule.manage')
    await scheduleService.insert(db, req, userid)
    return MessageResponse(message='Insert Success')

@router.post('/update', response_model=MessageResponse)
async def update(req: ScheduleUpdateRequest, request: Request, db: AsyncSession = Depends(get_db)):
    try:
        userid = await require_permission(request, db, 'schedule.manage')
        await scheduleService.update(db, req, userid)
        return MessageResponse(message='Update Success')
    except ValueError:
        raise HTTPException(404, 'Not found')

@router.post('/delete', response_model=MessageResponse)
async def delete(req: ScheduleDeleteRequest, request: Request, db: AsyncSession = Depends(get_db)):
    await require_permission(request, db, 'schedule.manage')
    await scheduleService.delete_obj(db, req)
    return MessageResponse(message='Delete Success')

