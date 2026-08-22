from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserInsertRequest(BaseModel):
    userid: str
    username: str
    nickname: str
    auth_cd: str
    phone: str

class UserUpdateRequest(BaseModel):
    userid: str
    ip: Optional[str] = None
    last_login_dt: Optional[datetime] = None
    use_yn: Optional[str] = None
    nickname: Optional[str] = None
    kakao_name: Optional[str] = None
    auth_cd: Optional[str] = None
    phone: Optional[str] = None
    update_dt: Optional[datetime] = None

