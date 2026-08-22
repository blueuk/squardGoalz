from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class TeamaccountResponse(BaseModel):
    team_uid: Optional[str] = None
    team_account_seq: Optional[str] = None
    bank_cd: Optional[str] = None
    account_enc: Optional[str] = None
    create_id: Optional[str] = None
    create_dt: Optional[str] = None
    update_id: Optional[str] = None
    update_dt: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class MessageResponse(BaseModel):
    message: str
