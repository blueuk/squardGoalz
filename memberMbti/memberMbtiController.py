from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from database import get_db
from auth import get_session_userid, require_self_or_permission
from memberMbti.memberMbtiRequest import MemberMbtiSearchRequest, MemberMbtiSaveRequest
from memberMbti.memberMbtiResponse import MemberMbtiResponse, MessageResponse
from memberMbti import memberMbtiService

router = APIRouter(prefix='/mbti', tags=['MemberMbti'])

@router.get('/search', response_model=List[MemberMbtiResponse])
async def search(request: Request, req: MemberMbtiSearchRequest = Depends(), db: AsyncSession = Depends(get_db)):
    """[로그인] 팀원들의 풋살 MBTI 결과를 조회합니다 (나와 잘 맞는 팀원 보기용)."""
    get_session_userid(request)
    return await memberMbtiService.get(db, req)

@router.post('/save', response_model=MessageResponse)
async def save(req: MemberMbtiSaveRequest, request: Request, db: AsyncSession = Depends(get_db)):
    """[본인 또는 권한: member.manage] 풋살 MBTI 결과를 저장합니다. 다시 테스트하면 덮어씁니다."""
    userid = await require_self_or_permission(request, db, req.team_uid, req.member_uid, 'member.manage')
    try:
        await memberMbtiService.save(db, req, userid)
        return MessageResponse(message='풋살 MBTI 저장 완료')
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
