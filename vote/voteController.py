from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from database import get_db
from auth import require_permission, require_self_or_permission
from vote.voteRequest import *
from vote.voteResponse import *
from vote import voteService

router = APIRouter(prefix='/vote', tags=['Vote'])

@router.get('/search', response_model=List[VoteResponse])
async def search(req: VoteSearchRequest = Depends(), db: AsyncSession = Depends(get_db)):
    return await voteService.get(db, req)

@router.post('/insert', response_model=MessageResponse)
async def insert(req: VoteInsertRequest, request: Request, db: AsyncSession = Depends(get_db)):
    userid = await require_permission(request, db, 'vote.manage')
    await voteService.insert(db, req, userid)
    return MessageResponse(message='Insert Success')

@router.post('/update', response_model=MessageResponse)
async def update(req: VoteUpdateRequest, request: Request, db: AsyncSession = Depends(get_db)):
    try:
        userid = await require_self_or_permission(request, db, req.team_uid, req.member_uid, 'vote.manage')
        await voteService.update(db, req, userid)
        return MessageResponse(message='Update Success')
    except ValueError:
        raise HTTPException(404, 'Not found')

@router.post('/delete', response_model=MessageResponse)
async def delete(req: VoteDeleteRequest, request: Request, db: AsyncSession = Depends(get_db)):
    await require_permission(request, db, 'vote.manage')
    await voteService.delete_obj(db, req)
    return MessageResponse(message='Delete Success')

