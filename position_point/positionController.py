from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from database import get_db
from position_point.positionRequest import (
    PositionPointSearchRequest, PositionPointInsertRequest,
    PositionPointUpdateRequest, PositionPointDeleteRequest
)
from position_point.positionResponse import PositionPointResponse, MessageResponse
from position_point import positionService

router = APIRouter(prefix="/position_point", tags=["PositionPoint"])

def get_session_userid(request: Request) -> str:
    userid = request.session.get("userid")
    if not userid:
        raise HTTPException(status_code=401, detail="로그인이 필요합니다.")
    return userid

@router.get("/search", response_model=List[PositionPointResponse])
async def search_position_points(req: PositionPointSearchRequest = Depends(), db: AsyncSession = Depends(get_db)):
    """GET 방식으로 position_point_b를 조회합니다."""
    try:
        return await positionService.get_position_points(db, req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/insert", response_model=MessageResponse)
async def insert_position_point(req: PositionPointInsertRequest, request: Request, db: AsyncSession = Depends(get_db)):
    """POST 방식으로 데이터를 등록하며 공통코드 존재 여부를 검증합니다."""
    userid = get_session_userid(request)
    try:
        await positionService.insert_position_point(db, req, userid)
        return MessageResponse(message="가중치 점수 등록 완료")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/update", response_model=MessageResponse)
async def update_position_point(req: PositionPointUpdateRequest, request: Request, db: AsyncSession = Depends(get_db)):
    """POST 방식으로 position_val 값을 업데이트합니다."""
    userid = get_session_userid(request)
    try:
        await positionService.update_position_point(db, req, userid)
        return MessageResponse(message="가중치 점수 수정 완료")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/delete", response_model=MessageResponse)
async def delete_position_point(req: PositionPointDeleteRequest, request: Request, db: AsyncSession = Depends(get_db)):
    """POST 방식으로 필수 키값(position_cd, score_cd)을 받아 삭제합니다."""
    get_session_userid(request) # 로그인 체크용
    try:
        await positionService.delete_position_point(db, req)
        return MessageResponse(message="가중치 점수 삭제 완료")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

