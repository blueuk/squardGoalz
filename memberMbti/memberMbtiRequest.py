from pydantic import BaseModel, Field
from typing import Optional, Literal

class MemberMbtiSearchRequest(BaseModel):
    team_uid: str
    member_uid: Optional[str] = None

class MemberMbtiSaveRequest(BaseModel):
    team_uid: str
    member_uid: str
    test_type: Literal['field', 'gk']
    mbti_cd: str
    fb_pct: Optional[int] = Field(None, ge=0, le=100)
    cw_pct: Optional[int] = Field(None, ge=0, le=100)
    pt_pct: int = Field(..., ge=0, le=100)
    sl_pct: int = Field(..., ge=0, le=100)
    answers: str
    question_ver: str
