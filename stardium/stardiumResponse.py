from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class StardiumResponse(BaseModel):
    team_uid: Optional[str] = None
    team_stardium_seq: Optional[str] = None
    location: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    day_cd: Optional[str] = None
    main_locate_yn: Optional[str] = None
    create_id: Optional[str] = None
    create_dt: Optional[str] = None
    update_id: Optional[str] = None
    update_dt: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class MessageResponse(BaseModel):
    message: str
