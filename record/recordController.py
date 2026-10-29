from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from database import get_db
from auth import get_admin_userid
from record.recordRequest import *
from record.recordResponse import *
from record import recordService

router = APIRouter(prefix='/record', tags=['Record'])

@router.get('/search', response_model=List[RecordResponse])
async def search(req: RecordSearchRequest = Depends(), db: AsyncSession = Depends(get_db)):
    return await recordService.get(db, req)

@router.post('/insert', response_model=MessageResponse)
async def insert(req: RecordInsertRequest, request: Request, db: AsyncSession = Depends(get_db)):
    userid = await get_admin_userid(request, db)
    await recordService.insert(db, req, userid)
    return MessageResponse(message='Insert Success')

@router.post('/update', response_model=MessageResponse)
async def update(req: RecordUpdateRequest, request: Request, db: AsyncSession = Depends(get_db)):
    try:
        userid = await get_admin_userid(request, db)
        await recordService.update(db, req, userid)
        return MessageResponse(message='Update Success')
    except ValueError:
        raise HTTPException(404, 'Not found')

@router.post('/delete', response_model=MessageResponse)
async def delete(req: RecordDeleteRequest, request: Request, db: AsyncSession = Depends(get_db)):
    await get_admin_userid(request, db)
    await recordService.delete_obj(db, req)
    return MessageResponse(message='Delete Success')

