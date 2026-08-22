from pydantic import BaseModel
from typing import Optional

class TeamarrangeSearchRequest(BaseModel):
    vote_uid: Optional[str] = None

class TeamarrangeInsertRequest(BaseModel):
    vote_uid: str
    play_date: Optional[str] = None
    team_cd: Optional[str] = None
    member_id: Optional[str] = None

class TeamarrangeUpdateRequest(BaseModel):
    vote_uid: str
    play_date: Optional[str] = None
    team_cd: Optional[str] = None
    member_id: Optional[str] = None

class TeamarrangeDeleteRequest(BaseModel):
    vote_uid: str
