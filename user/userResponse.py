from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class UserBResponse(BaseModel):
    userid: str
    username: Optional[str] = None
    ip: Optional[str] = None
    last_login_dt: Optional[datetime] = None
    use_yn: Optional[str] = None
    nickname: Optional[str] = None
    kakao_name: Optional[str] = None
    auth_cd: Optional[str] = None
    phone: Optional[str] = None
    create_dt: Optional[datetime] = None
    update_dt: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class MessageResponse(BaseModel):
    message: str

