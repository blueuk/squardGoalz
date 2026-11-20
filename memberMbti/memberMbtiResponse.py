from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class MemberMbtiResponse(BaseModel):
    team_uid: str
    member_uid: str
    test_type: str
    mbti_cd: str
    fb_pct: Optional[int] = None
    cw_pct: Optional[int] = None
    pt_pct: Optional[int] = None
    sl_pct: Optional[int] = None
    question_ver: Optional[str] = None
    update_dt: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class MessageResponse(BaseModel):
    message: str
