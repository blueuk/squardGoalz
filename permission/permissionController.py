from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from auth import get_session_userid, get_admin_userid, get_auth_cd, get_permissions, is_member_linked, ADMIN_AUTH_CD
from permission.permissionRequest import PermissionSaveRequest
from permission.permissionResponse import MyPermissionResponse, PermissionMatrixResponse, MessageResponse
from permission import permissionService

router = APIRouter(prefix="/permission", tags=["Permission"])

@router.get("/me", response_model=MyPermissionResponse)
async def get_my_permissions(request: Request, db: AsyncSession = Depends(get_db)):
    """[로그인] 내 역할과 기능 권한 목록"""
    userid = get_session_userid(request)
    auth_cd = await get_auth_cd(db, userid)
    return MyPermissionResponse(
        userid=userid,
        auth_cd=auth_cd,
        permissions=await get_permissions(db, userid),
        # 관리자는 선수가 아니어도 승인 대기 아님
        approved=auth_cd == ADMIN_AUTH_CD or await is_member_linked(db, userid),
    )

@router.get("/matrix", response_model=PermissionMatrixResponse)
async def get_matrix(request: Request, db: AsyncSession = Depends(get_db)):
    """[관리자] 권한 목록, 역할 목록, 역할별 부여 현황"""
    await get_admin_userid(request, db)
    return await permissionService.get_matrix(db)

@router.post("/save", response_model=MessageResponse)
async def save_role_permissions(req: PermissionSaveRequest, request: Request, db: AsyncSession = Depends(get_db)):
    """[관리자] 역할의 기능 권한을 저장(교체)합니다."""
    userid = await get_admin_userid(request, db)
    try:
        await permissionService.save_role_permissions(db, req, userid)
        return MessageResponse(message="권한이 저장되었습니다.")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
