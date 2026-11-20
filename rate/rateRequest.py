from pydantic import BaseModel
from typing import Optional

class RateSearchRequest(BaseModel):
    team_uid: Optional[str] = None
    teamname: Optional[str] = None
    member_uid: Optional[str] = None
    member_name: Optional[str] = None
    year: str
    today: Optional[str] = None  # YYYYMMDD, 연속 기록은 이 날짜 이전 경기만 (없으면 서버 기준 한국 날짜)

