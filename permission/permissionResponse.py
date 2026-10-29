from pydantic import BaseModel
from typing import List, Optional

class MyPermissionResponse(BaseModel):
    userid: str
    auth_cd: Optional[str] = None
    permissions: List[str]

class PermissionItemResponse(BaseModel):
    perm_cd: str
    screen: str
    name: str
    description: str

class RoleResponse(BaseModel):
    auth_cd: str
    name: str
    locked: bool  # 관리자: 항상 전체 권한 (수정 불가)

class PermissionMatrixResponse(BaseModel):
    permissions: List[PermissionItemResponse]
    roles: List[RoleResponse]
    grants: dict  # { auth_cd: [perm_cd, ...] }

class MessageResponse(BaseModel):
    message: str
