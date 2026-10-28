from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from database import get_db
from models.UserB import UserB
from teamArrange.teamArrangeRequest import *
from teamArrange.teamArrangeResponse import *
from teamArrange import teamArrangeService

router = APIRouter(prefix='/teamArrange', tags=['Teamarrange'])

def get_session_userid(request: Request) -> str:
    userid = request.session.get("userid")
    if not userid:
        raise HTTPException(status_code=401, detail="로그인이 필요합니다.")
    return userid

async def get_admin_userid(request: Request, db: AsyncSession) -> str:
    userid = get_session_userid(request)
    result = await db.execute(select(UserB.auth_cd).where(UserB.userid == userid))
    if result.scalar() != "01":  # 01: 관리자
        raise HTTPException(status_code=403, detail="관리자만 접근할 수 있습니다.")
    return userid

@router.get('/search', response_model=List[TeamarrangeResponse])
async def search(req: TeamarrangeSearchRequest = Depends(), db: AsyncSession = Depends(get_db)):
    """일정(team_uid, vote_seq)의 팀 배정 이력을 팀번호, 키퍼순서 순으로 조회합니다."""
    return await teamArrangeService.get(db, req)

@router.post('/save', response_model=MessageResponse)
async def save(req: TeamarrangeSaveRequest, request: Request, db: AsyncSession = Depends(get_db)):
    """[관리자] 일정의 팀 배정을 저장합니다. 기존 배정이 있으면 교체합니다."""
    userid = await get_admin_userid(request, db)
    try:
        await teamArrangeService.save(db, req, userid)
        return MessageResponse(message=f'{len(req.members)}명 팀 배정 저장 완료')
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/delete', response_model=MessageResponse)
async def delete(req: TeamarrangeDeleteRequest, request: Request, db: AsyncSession = Depends(get_db)):
    """[관리자] 일정의 팀 배정 이력을 삭제합니다."""
    await get_admin_userid(request, db)
    try:
        await teamArrangeService.delete_obj(db, req)
        return MessageResponse(message='팀 배정 삭제 완료')
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
