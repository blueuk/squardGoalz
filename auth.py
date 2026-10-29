"""공통 인증 / 권한 확인"""
from fastapi import HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.UserB import UserB
from models.TeamMemberL import TeamMemberL
from models.AuthRolePermissionL import AuthRolePermissionL
from permission.permissionCatalog import ALL_CODES

ADMIN_AUTH_CD = "01"  # 관리자

def get_session_userid(request: Request) -> str:
    userid = request.session.get("userid")
    if not userid:
        raise HTTPException(status_code=401, detail="로그인이 필요합니다.")
    return userid

async def get_auth_cd(db: AsyncSession, userid: str):
    result = await db.execute(select(UserB.auth_cd).where(UserB.userid == userid))
    return result.scalar()

async def get_admin_userid(request: Request, db: AsyncSession) -> str:
    userid = get_session_userid(request)
    if await get_auth_cd(db, userid) != ADMIN_AUTH_CD:
        raise HTTPException(status_code=403, detail="관리자만 접근할 수 있습니다.")
    return userid

async def get_permissions(db: AsyncSession, userid: str) -> list:
    """유저의 기능 권한 목록 (관리자는 전체)"""
    auth_cd = await get_auth_cd(db, userid)
    if auth_cd == ADMIN_AUTH_CD:
        return list(ALL_CODES)
    if not auth_cd:
        return []
    result = await db.execute(select(AuthRolePermissionL.perm_cd).where(AuthRolePermissionL.auth_cd == auth_cd))
    return list(result.scalars().all())

async def has_permission(db: AsyncSession, userid: str, perm_cd: str) -> bool:
    return perm_cd in await get_permissions(db, userid)

async def require_permission(request: Request, db: AsyncSession, perm_cd: str) -> str:
    """로그인 + 기능 권한 확인. 통과하면 userid 반환"""
    userid = get_session_userid(request)
    if not await has_permission(db, userid, perm_cd):
        raise HTTPException(status_code=403, detail="이 기능을 사용할 권한이 없습니다.")
    return userid

async def require_self_or_permission(request: Request, db: AsyncSession, team_uid: str, member_uid: str, perm_cd: str) -> str:
    """본인(멤버와 연결된 유저)이면 통과, 아니면 기능 권한 확인. 통과하면 userid 반환"""
    userid = get_session_userid(request)
    owner = (await db.execute(
        select(TeamMemberL.user_id).where(TeamMemberL.team_uid == team_uid, TeamMemberL.member_uid == member_uid)
    )).scalar()
    if owner and owner == userid:
        return userid
    return await require_permission(request, db, perm_cd)
