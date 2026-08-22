from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from database import get_db
from teamInfo.teamInfoRequest import (
    TeamInfoSearchRequest, TeamInfoInsertRequest,
    TeamInfoUpdateRequest, TeamInfoDeleteRequest
)
from teamInfo.teamInfoResponse import TeamInfoResponse, MessageResponse
from teamInfo import teamInfoService

router = APIRouter(prefix="/team_info", tags=["TeamInfo"])

def get_session_userid(request: Request) -> str:
    userid = request.session.get("userid")
    if not userid:
        raise HTTPException(status_code=401, detail="로그인이 필요합니다.")
    return userid

@router.get("/search", response_model=List[TeamInfoResponse])
async def search_team_info(req: TeamInfoSearchRequest = Depends(), db: AsyncSession = Depends(get_db)):
    """GET 방식으로 팀 정보 리스트를 조회합니다."""
    try:
        return await teamInfoService.get_team_info(db, req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/insert", response_model=MessageResponse)
async def insert_team_info(req: TeamInfoInsertRequest, request: Request, db: AsyncSession = Depends(get_db)):
    """POST 방식으로 새로운 팀을 생성합니다 (팀 UID 자동 발급)."""
    userid = get_session_userid(request)
    try:
        await teamInfoService.insert_team_info(db, req, userid)
        return MessageResponse(message="팀 정보 등록 완료")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/update", response_model=MessageResponse)
async def update_team_info(req: TeamInfoUpdateRequest, request: Request, db: AsyncSession = Depends(get_db)):
    """POST 방식으로 기존 팀 정보를 수정합니다."""
    userid = get_session_userid(request)
    try:
        await teamInfoService.update_team_info(db, req, userid)
        return MessageResponse(message="팀 정보 수정 완료")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/delete", response_model=MessageResponse)
async def delete_team_info(req: TeamInfoDeleteRequest, request: Request, db: AsyncSession = Depends(get_db)):
    """POST 방식으로 기존 팀 정보를 삭제합니다."""
    get_session_userid(request)
    try:
        await teamInfoService.delete_team_info(db, req)
        return MessageResponse(message="팀 정보 삭제 완료")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

