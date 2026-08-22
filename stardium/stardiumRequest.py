from pydantic import BaseModel
from typing import Optional

class StardiumSearchRequest(BaseModel):
    team_uid: Optional[str] = None
    team_stardium_seq: Optional[str] = None

class StardiumInsertRequest(BaseModel):
    team_uid: str
    location: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    day_cd: Optional[str] = None
    main_locate_yn: Optional[str] = None

class StardiumUpdateRequest(BaseModel):
    team_uid: str
    team_stardium_seq: int
    location: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    day_cd: Optional[str] = None
    main_locate_yn: Optional[str] = None

class StardiumDeleteRequest(BaseModel):
    team_uid: str
    team_stardium_seq: int
