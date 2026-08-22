from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from database import get_db
from stardium.stardiumRequest import *
from stardium.stardiumResponse import *
from stardium import stardiumService

router = APIRouter(prefix='/stardium', tags=['Stardium'])

def get_session_userid(request: Request) -> str:
    return request.session.get('userid', 'test_user')

@router.get('/search', response_model=List[StardiumResponse])
async def search(req: StardiumSearchRequest = Depends(), db: AsyncSession = Depends(get_db)):
    return await stardiumService.get(db, req)

@router.post('/insert', response_model=MessageResponse)
async def insert(req: StardiumInsertRequest, request: Request, db: AsyncSession = Depends(get_db)):
    await stardiumService.insert(db, req, get_session_userid(request))
    return MessageResponse(message='Insert Success')

@router.post('/update', response_model=MessageResponse)
async def update(req: StardiumUpdateRequest, request: Request, db: AsyncSession = Depends(get_db)):
    try:
        await stardiumService.update(db, req, get_session_userid(request))
        return MessageResponse(message='Update Success')
    except ValueError:
        raise HTTPException(404, 'Not found')

@router.post('/delete', response_model=MessageResponse)
async def delete(req: StardiumDeleteRequest, request: Request, db: AsyncSession = Depends(get_db)):
    await stardiumService.delete_obj(db, req)
    return MessageResponse(message='Delete Success')

