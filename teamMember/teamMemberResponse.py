from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class TeamMemberResponse(BaseModel):
    team_uid: str
    teamname: Optional[str] = None  # team_info_b와 Join하여 반환될 팀명
    member_uid: str
    member_name: Optional[str] = None
    user_id: Optional[str] = None
    sign_dt: Optional[str] = None
    gender_cd: Optional[str] = None
    status_cd: Optional[str] = None
    terminate_dt: Optional[str] = None
    create_id: Optional[str] = None
    create_dt: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

class MessageResponse(BaseModel):
    message: str

