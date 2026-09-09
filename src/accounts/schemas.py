from pydantic import BaseModel, Field
import uuid
from datetime import datetime
from decimal import Decimal
from src.db.models import StatusType

class AccountModel(BaseModel):
    account_number: str
    user_id: uuid.UUID
    created_at: datetime 
    status: StatusType
    balance: Decimal 

class AccountStatusUpdateModel(BaseModel):
    status: StatusType