from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class MemberscoreResponse(BaseModel):
    member_uid: Optional[str] = None
    team_uid: Optional[str] = None
    year: Optional[str] = None
    score_cd: Optional[str] = None
    score_val: Optional[str] = None
    create_id: Optional[str] = None
    create_dt: Optional[str] = None
    update_id: Optional[str] = None
    update_dt: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class MessageResponse(BaseModel):
    message: str
