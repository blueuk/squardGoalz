from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class CommonGroupCdResponse(BaseModel):
    group_cd: str
    group_name: Optional[str] = None
    use_yn: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    create_id: Optional[str] = None
    create_dt: Optional[datetime] = None
    update_id: Optional[str] = None
    update_dt: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

class CommonCdResponse(BaseModel):
    group_cd: str
    code: str
    code_name: Optional[str] = None
    code_seq: Optional[int] = None
    reference_1: Optional[str] = None
    reference_2: Optional[str] = None
    reference_3: Optional[str] = None
    reference_4: Optional[str] = None
    use_yn: Optional[str] = None
    create_id: Optional[str] = None
    create_dt: Optional[datetime] = None
    update_id: Optional[str] = None
    update_dt: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

class MessageResponse(BaseModel):
    message: str

