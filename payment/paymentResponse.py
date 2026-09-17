from pydantic import BaseModel, ConfigDict
from typing import Optional, Any
from datetime import datetime
from decimal import Decimal

class PaymentResponse(BaseModel):
    team_uid: Optional[str] = None
    payment_cd: Optional[str] = None
    team_account_seq: Optional[int] = None
    amount: Optional[Decimal] = None
    create_id: Optional[str] = None
    create_dt: Optional[datetime] = None
    update_id: Optional[str] = None
    update_dt: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class MessageResponse(BaseModel):
    message: str
