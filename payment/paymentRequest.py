from pydantic import BaseModel
from typing import Optional

class PaymentSearchRequest(BaseModel):
    team_uid: Optional[str] = None
    payment_cd: Optional[str] = None
    team_account_seq: Optional[str] = None

class PaymentInsertRequest(BaseModel):
    team_uid: str
    payment_cd: str
    team_account_seq: str
    amount: Optional[str] = None

class PaymentUpdateRequest(BaseModel):
    team_uid: str
    payment_cd: str
    team_account_seq: str
    amount: Optional[str] = None

class PaymentDeleteRequest(BaseModel):
    team_uid: str
    payment_cd: str
    team_account_seq: str
