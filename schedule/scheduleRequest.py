from pydantic import BaseModel
from typing import Optional

class ScheduleSearchRequest(BaseModel):
    vote_seq: Optional[str] = None
    team_uid: Optional[str] = None

class ScheduleInsertRequest(BaseModel):
    team_uid: str
    play_date: Optional[str] = None
    play_start_time: Optional[str] = None
    play_end_time: Optional[str] = None
    vote_period_from: Optional[str] = None
    vote_period_to: Optional[str] = None
    vote_end_yn: Optional[str] = None

class ScheduleUpdateRequest(BaseModel):
    vote_seq: int
    team_uid: str
    play_date: Optional[str] = None
    play_start_time: Optional[str] = None
    play_end_time: Optional[str] = None
    vote_period_from: Optional[str] = None
    vote_period_to: Optional[str] = None
    vote_end_yn: Optional[str] = None

class ScheduleDeleteRequest(BaseModel):
    vote_seq: int
    team_uid: str
