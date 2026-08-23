from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from database import get_db
from rate.rateRequest import RateSearchRequest
from rate.rateResponse import RateResponse
from rate import rateService

router = APIRouter(prefix="/rate", tags=["Rate"])

@router.get("/search", response_model=List[RateResponse])
async def search_rates(req: RateSearchRequest = Depends(), db: AsyncSession = Depends(get_db)):
    """GET 방식으로 해당 연도의 멤버 참석률 및 순위를 조회합니다."""
    try:
        return await rateService.get_rates(db, req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

