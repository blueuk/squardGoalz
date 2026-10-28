from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from database import get_db
from models.UserB import UserB
from position_point.positionRequest import (
    PositionPointSearchRequest, PositionPointInsertRequest,
    PositionPointUpdateRequest, PositionPointDeleteRequest,
    PositionPointBulkUpsertRequest, ScoreItemInsertRequest, ScoreItemDeleteRequest
)
from position_point.positionResponse import PositionPointResponse, MessageResponse, ScoreItemResponse
from position_point import positionService

router = APIRouter(prefix="/position_point", tags=["PositionPoint"])

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

@router.get("/search", response_model=List[PositionPointResponse])
async def search_position_points(req: PositionPointSearchRequest = Depends(), db: AsyncSession = Depends(get_db)):
    """GET 방식으로 position_point_b를 조회합니다."""
    try:
        return await positionService.get_position_points(db, req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/insert", response_model=MessageResponse)
async def insert_position_point(req: PositionPointInsertRequest, request: Request, db: AsyncSession = Depends(get_db)):
    """POST 방식으로 데이터를 등록합니다."""
    userid = get_session_userid(request)
    try:
        await positionService.insert_position_point(db, req, userid)
        return MessageResponse(message="가중치 점수 등록 완료")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upsert", response_model=MessageResponse)
async def upsert_position_point(req: PositionPointUpdateRequest, request: Request, db: AsyncSession = Depends(get_db)):
    """POST 방식으로 position_cd + score_cd 키로 upsert합니다."""
    userid = get_session_userid(request)
    try:
        await positionService.upsert_position_point(db, req, userid)
        return MessageResponse(message="가중치 점수 upsert 완료")
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/bulk_upsert", response_model=MessageResponse)
async def bulk_upsert_position_points(req: PositionPointBulkUpsertRequest, request: Request, db: AsyncSession = Depends(get_db)):
    """[관리자] 변경된 가중치를 한 번의 트랜잭션으로 일괄 upsert합니다."""
    userid = await get_admin_userid(request, db)
    try:
        await positionService.bulk_upsert_position_points(db, req.items, userid)
        return MessageResponse(message=f"{len(req.items)}개 가중치 저장 완료")
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
    get_session_userid(request)
    try:
        await positionService.delete_position_point(db, req)
        return MessageResponse(message="가중치 점수 삭제 완료")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/score_item/insert", response_model=ScoreItemResponse)
async def insert_score_item(req: ScoreItemInsertRequest, request: Request, db: AsyncSession = Depends(get_db)):
    """[관리자] 능력치(가중치) 항목을 추가합니다. 모든 포지션 가중치 0, 선수단 전원 기본점수 10점."""
    userid = await get_admin_userid(request, db)
    try:
        return await positionService.insert_score_item(db, req, userid)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/score_item/delete", response_model=MessageResponse)
async def delete_score_item(req: ScoreItemDeleteRequest, request: Request, db: AsyncSession = Depends(get_db)):
    """[관리자] 능력치(가중치) 항목과 연결된 가중치 / 선수 점수를 삭제합니다."""
    await get_admin_userid(request, db)
    try:
        await positionService.delete_score_item(db, req)
        return MessageResponse(message="능력치 항목 삭제 완료")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
