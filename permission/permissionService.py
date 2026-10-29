from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from datetime import datetime
from models.AuthRolePermissionL import AuthRolePermissionL
from models.CommonCdB import CommonCdB
from permission.permissionCatalog import PERMISSIONS, GRANTABLE_CODES, ALL_CODES
from permission import permissionRequest
from auth import ADMIN_AUTH_CD

async def get_matrix(db: AsyncSession):
    roles = (await db.execute(
        select(CommonCdB).where(CommonCdB.group_cd == 'auth_cd').order_by(CommonCdB.code_seq.asc(), CommonCdB.code.asc())
    )).scalars().all()
    rows = (await db.execute(select(AuthRolePermissionL))).scalars().all()

    grants = {r.code: [] for r in roles}
    for row in rows:
        grants.setdefault(row.auth_cd, []).append(row.perm_cd)
    grants[ADMIN_AUTH_CD] = list(ALL_CODES)

    return {
        'permissions': [
            {'perm_cd': code, 'screen': screen, 'name': name, 'description': desc}
            for code, screen, name, desc in PERMISSIONS
        ],
        'roles': [{'auth_cd': r.code, 'name': r.code_name, 'locked': r.code == ADMIN_AUTH_CD} for r in roles],
        'grants': grants,
    }

async def save_role_permissions(db: AsyncSession, req: permissionRequest.PermissionSaveRequest, session_id: str):
    """역할의 권한을 요청 목록으로 통째로 교체합니다."""
    if req.auth_cd == ADMIN_AUTH_CD:
        raise ValueError("관리자 권한은 변경할 수 없습니다.")
    role = (await db.execute(
        select(CommonCdB).where(CommonCdB.group_cd == 'auth_cd', CommonCdB.code == req.auth_cd)
    )).scalars().first()
    if not role:
        raise ValueError("존재하지 않는 역할입니다.")
    invalid = [p for p in req.perm_cds if p not in GRANTABLE_CODES]
    if invalid:
        raise ValueError(f"부여할 수 없는 권한입니다: {', '.join(invalid)}")

    await db.execute(delete(AuthRolePermissionL).where(AuthRolePermissionL.auth_cd == req.auth_cd))
    now = datetime.now()
    for perm_cd in dict.fromkeys(req.perm_cds):
        db.add(AuthRolePermissionL(auth_cd=req.auth_cd, perm_cd=perm_cd, create_id=session_id, create_dt=now))
    await db.commit()
