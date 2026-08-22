from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class PositionPointResponse(BaseModel):
    position_cd: str
    score_cd: str
    position_val: Optional[float] = None
    create_id: Optional[str] = None
    create_dt: Optional[datetime] = None
    update_id: Optional[str] = None
    update_dt: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

class MessageResponse(BaseModel):
    message: str

