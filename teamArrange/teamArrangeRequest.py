from pydantic import BaseModel
from typing import Optional, List

class TeamarrangeSearchRequest(BaseModel):
    team_uid: Optional[str] = None
    vote_seq: Optional[int] = None

class TeamarrangeMemberItemRequest(BaseModel):
    member_uid: str
    member_name: str
    merc_yn: str = 'N'
    team_no: int
    keeper_order: int

class TeamarrangeSaveRequest(BaseModel):
    team_uid: str
    vote_seq: int
    members: List[TeamarrangeMemberItemRequest]

class TeamarrangeDeleteRequest(BaseModel):
    team_uid: str
    vote_seq: int
