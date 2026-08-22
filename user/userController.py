from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from database import get_db
from user.userRequest import UserInsertRequest, UserUpdateRequest
from user.userResponse import UserBResponse, MessageResponse
from user import userService

router = APIRouter(prefix="/user", tags=["User"])

@router.post("/insert", response_model=MessageResponse)
async def insert_user(req: UserInsertRequest, db: AsyncSession = Depends(get_db)):
    """카카오 로그인 후 받아온 정보로 유저 등록 (UserB, UserH 동시 등록)"""
    try:
        existing_users = await userService.get_users(db, userid=req.userid)
        if existing_users:
            raise HTTPException(status_code=400, detail="이미 등록된 아이디입니다.")
            
        await userService.insert_user(db, req)
        return MessageResponse(message="유저 등록 및 이력 저장이 완료되었습니다.")
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"유저 등록 중 오류 발생: {str(e)}")

@router.get("/get", response_model=List[UserBResponse])
async def get_users(
    userid: Optional[str] = None,
    username: Optional[str] = None,
    nickname: Optional[str] = None,
    phone: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """지정된 조건(userid, username, nickname, phone)으로 UserB 목록 조회"""
    try:
        users = await userService.get_users(db, userid, username, nickname, phone)
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"조회 중 오류 발생: {str(e)}")

@router.post("/update", response_model=MessageResponse)
async def update_user(req: UserUpdateRequest, db: AsyncSession = Depends(get_db)):
    """UserB 정보를 업데이트하고 해당 이력을 UserH에 새로 삽입"""
    try:
        updated_user = await userService.update_user(db, req)
        if not updated_user:
            raise HTTPException(status_code=404, detail="해당 아이디를 가진 유저를 찾을 수 없습니다.")
        return MessageResponse(message="유저 정보 수정 및 이력 등록이 완료되었습니다.")
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"수정 중 오류 발생: {str(e)}")

@router.delete("/delete/{userid}", response_model=MessageResponse)
async def delete_user(userid: str, db: AsyncSession = Depends(get_db)):
    """UserB 정보를 삭제하고 연결된 UserH 이력도 모두 삭제합니다."""
    try:
        is_deleted = await userService.delete_user(db, userid)
        if not is_deleted:
            raise HTTPException(status_code=404, detail="해당 아이디를 가진 유저를 찾을 수 없습니다.")
        return MessageResponse(message=f"유저({userid}) 및 관련 이력이 모두 삭제되었습니다.")
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"삭제 중 오류 발생: {str(e)}")
