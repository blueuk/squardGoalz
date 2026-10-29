from pydantic import BaseModel
from typing import List

class PermissionSaveRequest(BaseModel):
    auth_cd: str
    perm_cds: List[str]
