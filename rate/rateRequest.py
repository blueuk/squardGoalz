from pydantic import BaseModel
from typing import Optional

class RateSearchRequest(BaseModel):
    team_uid: Optional[str] = None
    teamname: Optional[str] = None
    member_uid: Optional[str] = None
    member_name: Optional[str] = None
    year: str

