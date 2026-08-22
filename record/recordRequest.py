from pydantic import BaseModel
from typing import Optional

class RecordSearchRequest(BaseModel):
    team_uid: Optional[str] = None
    vote_uid: Optional[str] = None
    play_date: Optional[str] = None

class RecordInsertRequest(BaseModel):
    team_uid: str
    vote_uid: str
    play_date: str
    member_uid: Optional[str] = None
    goal_cnt: Optional[str] = None
    asist_cnt: Optional[str] = None

class RecordUpdateRequest(BaseModel):
    team_uid: str
    vote_uid: str
    play_date: str
    member_uid: Optional[str] = None
    goal_cnt: Optional[str] = None
    asist_cnt: Optional[str] = None

class RecordDeleteRequest(BaseModel):
    team_uid: str
    vote_uid: str
    play_date: str
