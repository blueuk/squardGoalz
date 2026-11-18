from pydantic import BaseModel
from typing import Optional, List

class TeamarrangeSearchRequest(BaseModel):
    team_uid: Optional[str] = None
    vote_seq: Optional[int] = None

class TeamarrangeNextRequest(BaseModel):
    team_uid: str
    today: str  # YYYYMMDD (사용자 기준 오늘: 서버 시간대와 무관하게 비교)

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
