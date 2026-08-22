from pydantic import BaseModel, Field
from typing import Optional

class TeamInfoSearchRequest(BaseModel):
    team_uid: Optional[str] = None
    teamname: Optional[str] = None
    region_cd: Optional[str] = None
    day_cd: Optional[str] = None
    level_cd: Optional[str] = None
    gender_cd: Optional[str] = None
    use_yn: Optional[str] = 'Y'

class TeamInfoInsertRequest(BaseModel):
    teamname: str
    region_cd: Optional[str] = None
    location: Optional[str] = None
    start_time: Optional[str] = Field(None, pattern=r"^(?:[01]\d|2[0-3])[0-5]\d$") # HH24MM validation
    end_time: Optional[str] = Field(None, pattern=r"^(?:[01]\d|2[0-3])[0-5]\d$")
    day_cd: Optional[str] = None
    level_cd: Optional[str] = None
    gender_cd: Optional[str] = None
    use_yn: str = 'Y'
    comment: Optional[str] = None

class TeamInfoUpdateRequest(BaseModel):
    team_uid: str
    teamname: Optional[str] = None
    region_cd: Optional[str] = None
    location: Optional[str] = None
    start_time: Optional[str] = Field(None, pattern=r"^(?:[01]\d|2[0-3])[0-5]\d$")
    end_time: Optional[str] = Field(None, pattern=r"^(?:[01]\d|2[0-3])[0-5]\d$")
    day_cd: Optional[str] = None
    level_cd: Optional[str] = None
    gender_cd: Optional[str] = None
    use_yn: Optional[str] = None
    comment: Optional[str] = None

class TeamInfoDeleteRequest(BaseModel):
    team_uid: str

