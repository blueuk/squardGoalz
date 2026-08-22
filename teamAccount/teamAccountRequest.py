from pydantic import BaseModel
from typing import Optional

class TeamaccountSearchRequest(BaseModel):
    team_uid: Optional[str] = None
    team_account_seq: Optional[str] = None
    bank_cd: Optional[str] = None
    account_enc: Optional[str] = None

class TeamaccountInsertRequest(BaseModel):
    team_uid: str
    bank_cd: str
    account_enc: str

class TeamaccountUpdateRequest(BaseModel):
    team_uid: str
    team_account_seq: int
    bank_cd: str
    account_enc: str

class TeamaccountDeleteRequest(BaseModel):
    team_uid: str
    team_account_seq: int
    bank_cd: str
    account_enc: str
