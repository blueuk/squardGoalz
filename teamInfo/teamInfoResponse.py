from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class TeamInfoResponse(BaseModel):
    team_uid: str
    teamname: Optional[str] = None
    region_cd: Optional[str] = None
    location: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    day_cd: Optional[str] = None
    level_cd: Optional[str] = None
    gender_cd: Optional[str] = None
    use_yn: Optional[str] = None
    comment: Optional[str] = None
    create_id: Optional[str] = None
    create_dt: Optional[datetime] = None
    update_id: Optional[str] = None
    update_dt: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

class MessageResponse(BaseModel):
    message: str

