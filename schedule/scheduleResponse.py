from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class ScheduleResponse(BaseModel):
    vote_seq: Optional[str] = None
    team_uid: Optional[str] = None
    play_date: Optional[str] = None
    play_start_time: Optional[str] = None
    play_end_time: Optional[str] = None
    vote_period_from: Optional[str] = None
    vote_period_to: Optional[str] = None
    vote_end_yn: Optional[str] = None
    create_id: Optional[str] = None
    create_dt: Optional[str] = None
    update_id: Optional[str] = None
    update_dt: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class MessageResponse(BaseModel):
    message: str
