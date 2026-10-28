from pydantic import BaseModel
from typing import Optional, List

class PositionPointSearchRequest(BaseModel):
    position_cd: Optional[str] = None
    score_cd: Optional[str] = None

class PositionPointInsertRequest(BaseModel):
    position_cd: str
    score_cd: str
    position_val: float

class PositionPointUpdateRequest(BaseModel):
    position_cd: str
    score_cd: str
    position_val: float

class PositionPointDeleteRequest(BaseModel):
    position_cd: str
    score_cd: str

class PositionPointBulkUpsertItemRequest(BaseModel):
    position_cd: str
    score_cd: str
    position_val: float

class PositionPointBulkUpsertRequest(BaseModel):
    items: List[PositionPointBulkUpsertItemRequest]

class ScoreItemInsertRequest(BaseModel):
    code_name: str
    category: Optional[str] = None  # 능력치 리포트 분류 (physical, technique, defense, mental, etc)

class ScoreItemDeleteRequest(BaseModel):
    score_cd: str
