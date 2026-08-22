from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from database import get_db
from vote.voteRequest import *
from vote.voteResponse import *
from vote import voteService

router = APIRouter(prefix='/vote', tags=['Vote'])

def get_session_userid(request: Request) -> str:
    return request.session.get('userid', 'test_user')

@router.get('/search', response_model=List[VoteResponse])
async def search(req: VoteSearchRequest = Depends(), db: AsyncSession = Depends(get_db)):
    return await voteService.get(db, req)

@router.post('/insert', response_model=MessageResponse)
async def insert(req: VoteInsertRequest, request: Request, db: AsyncSession = Depends(get_db)):
    await voteService.insert(db, req, get_session_userid(request))
    return MessageResponse(message='Insert Success')

@router.post('/update', response_model=MessageResponse)
async def update(req: VoteUpdateRequest, request: Request, db: AsyncSession = Depends(get_db)):
    try:
        await voteService.update(db, req, get_session_userid(request))
        return MessageResponse(message='Update Success')
    except ValueError:
        raise HTTPException(404, 'Not found')

@router.post('/delete', response_model=MessageResponse)
async def delete(req: VoteDeleteRequest, request: Request, db: AsyncSession = Depends(get_db)):
    await voteService.delete_obj(db, req)
    return MessageResponse(message='Delete Success')

