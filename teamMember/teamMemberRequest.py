from pydantic import BaseModel
from typing import Optional, List

class TeamMemberSearchRequest(BaseModel):
    team_uid: Optional[str] = None
    teamname: Optional[str] = None
    member_name: Optional[str] = None

class TeamMemberItemRequest(BaseModel):
    team_uid: str
    member_name: str
    user_id: Optional[str] = None
    gender_cd: Optional[str] = None
    status_cd: Optional[str] = "01" # 01: 활동 (기본값)
    
class TeamMemberInsertRequest(BaseModel):
    members: List[TeamMemberItemRequest]

class TeamMemberUpdateRequest(BaseModel):
    team_uid: str
    member_uid: str
    member_name: Optional[str] = None
    user_id: Optional[str] = None
    gender_cd: Optional[str] = None
    status_cd: Optional[str] = None

class TeamMemberTerminateRequest(BaseModel):
    team_uid: str
    member_uid: str

