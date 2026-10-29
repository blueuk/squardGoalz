from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from database import get_db
from auth import require_permission
from memberScore.memberScoreRequest import *
from memberScore.memberScoreResponse import *
from memberScore import memberScoreService

router = APIRouter(prefix='/memberScore', tags=['Memberscore'])

@router.get('/search', response_model=List[MemberscoreResponse])
async def search(req: MemberscoreSearchRequest = Depends(), db: AsyncSession = Depends(get_db)):
    return await memberScoreService.get(db, req)

@router.post('/insert', response_model=MessageResponse)
async def insert(req: MemberscoreInsertRequest, request: Request, db: AsyncSession = Depends(get_db)):
    userid = await require_permission(request, db, 'score.edit')
    await memberScoreService.insert(db, req, userid)
    return MessageResponse(message='Insert Success')

@router.post('/update', response_model=MessageResponse)
async def update(req: MemberscoreUpdateRequest, request: Request, db: AsyncSession = Depends(get_db)):
    try:
        userid = await require_permission(request, db, 'score.edit')
        await memberScoreService.update(db, req, userid)
        return MessageResponse(message='Update Success')
    except ValueError:
        raise HTTPException(404, 'Not found')

@router.post('/delete', response_model=MessageResponse)
async def delete(req: MemberscoreDeleteRequest, request: Request, db: AsyncSession = Depends(get_db)):
    await require_permission(request, db, 'score.edit')
    await memberScoreService.delete_obj(db, req)
    return MessageResponse(message='Delete Success')

