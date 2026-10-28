from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class TeamarrangeResponse(BaseModel):
    team_uid: str
    vote_seq: int
    member_uid: str
    member_name: Optional[str] = None
    merc_yn: Optional[str] = None
    team_no: Optional[int] = None
    keeper_order: Optional[int] = None
    play_date: Optional[str] = None
    create_id: Optional[str] = None
    create_dt: Optional[datetime] = None
    update_id: Optional[str] = None
    update_dt: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class MessageResponse(BaseModel):
    message: str
