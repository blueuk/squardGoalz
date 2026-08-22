from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from database import get_db
from common_cd.commonCdRequest import (
    CommonGroupCdSearchRequest, CommonGroupCdInsertRequest, CommonGroupCdUpdateRequest,
    CommonCdSearchRequest, CommonCdInsertRequest, CommonCdUpdateRequest
)
from common_cd.commonCdResponse import CommonGroupCdResponse, CommonCdResponse, MessageResponse
from common_cd import commonCdService

router = APIRouter(prefix="/common_cd", tags=["CommonCode"])

def get_session_userid(request: Request) -> str:
    userid = request.session.get("userid")
    if not userid:
        # 로그인 세션이 없을 경우 에러 처리 (현재는 더미 아이디 활용 방어코드)
        raise HTTPException(status_code=401, detail="로그인이 필요합니다.")
    return userid

# ================= 그룹 코드 API =================

@router.get("/group/search", response_model=List[CommonGroupCdResponse])
async def search_group_codes(req: CommonGroupCdSearchRequest = Depends(), db: AsyncSession = Depends(get_db)):
    try:
        return await commonCdService.get_group_codes(db, req)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/group/insert", response_model=MessageResponse)
async def insert_group_code(req: CommonGroupCdInsertRequest, request: Request, db: AsyncSession = Depends(get_db)):
    userid = get_session_userid(request)
    try:
        await commonCdService.insert_group_code(db, req, userid)
        return MessageResponse(message="공통코드 그룹 등록 완료")
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/group/update", response_model=MessageResponse)
async def update_group_code(req: CommonGroupCdUpdateRequest, request: Request, db: AsyncSession = Depends(get_db)):
    userid = get_session_userid(request)
    try:
        await commonCdService.update_group_code(db, req, userid)
        return MessageResponse(message="공통코드 그룹 수정 완료")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# ================= 상세 코드 API =================

@router.get("/search", response_model=List[CommonCdResponse])
async def search_common_codes(req: CommonCdSearchRequest = Depends(), db: AsyncSession = Depends(get_db)):
    try:
        return await commonCdService.get_common_codes(db, req)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/insert", response_model=MessageResponse)
async def insert_common_code(req: CommonCdInsertRequest, request: Request, db: AsyncSession = Depends(get_db)):
    userid = get_session_userid(request)
    try:
        await commonCdService.insert_common_code(db, req, userid)
        return MessageResponse(message="공통코드 등록 완료")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/update", response_model=MessageResponse)
async def update_common_code(req: CommonCdUpdateRequest, request: Request, db: AsyncSession = Depends(get_db)):
    userid = get_session_userid(request)
    try:
        await commonCdService.update_common_code(db, req, userid)
        return MessageResponse(message="공통코드 수정 완료")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

