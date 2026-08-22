from pydantic import BaseModel
from typing import Optional

class VoteSearchRequest(BaseModel):
    vote_seq: Optional[str] = None
    team_uid: Optional[str] = None

class VoteInsertRequest(BaseModel):
    vote_seq: str
    team_uid: str
    play_date: Optional[str] = None
    play_start_time: Optional[str] = None
    play_end_time: Optional[str] = None
    member_uid: Optional[str] = None
    vote_cd: Optional[str] = None

class VoteUpdateRequest(BaseModel):
    vote_seq: str
    team_uid: str
    play_date: Optional[str] = None
    play_start_time: Optional[str] = None
    play_end_time: Optional[str] = None
    member_uid: Optional[str] = None
    vote_cd: Optional[str] = None

class VoteDeleteRequest(BaseModel):
    vote_seq: str
    team_uid: str
