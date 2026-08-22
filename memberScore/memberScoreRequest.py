from pydantic import BaseModel
from typing import Optional

class MemberscoreSearchRequest(BaseModel):
    member_uid: Optional[str] = None
    team_uid: Optional[str] = None
    year: Optional[str] = None
    score_cd: Optional[str] = None

class MemberscoreInsertRequest(BaseModel):
    member_uid: str
    team_uid: str
    year: str
    score_cd: str
    score_val: Optional[str] = None

class MemberscoreUpdateRequest(BaseModel):
    member_uid: str
    team_uid: str
    year: str
    score_cd: str
    score_val: Optional[str] = None

class MemberscoreDeleteRequest(BaseModel):
    member_uid: str
    team_uid: str
    year: str
    score_cd: str
