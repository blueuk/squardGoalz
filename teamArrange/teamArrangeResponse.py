from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class TeamarrangeResponse(BaseModel):
    vote_uid: Optional[str] = None
    play_date: Optional[str] = None
    team_cd: Optional[str] = None
    member_id: Optional[str] = None
    create_id: Optional[str] = None
    create_dt: Optional[str] = None
    update_id: Optional[str] = None
    update_dt: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class MessageResponse(BaseModel):
    message: str
