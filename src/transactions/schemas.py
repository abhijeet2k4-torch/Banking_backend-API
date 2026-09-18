from decimal import Decimal
from pydantic import BaseModel, Field
import uuid
from datetime import datetime
from src.db.models import TransactionType


class TransactionModel(BaseModel):
    transaction_id: uuid.UUID 
    sender_account_number: str | None
    receiver_account_number: str | None
    transaction_type: TransactionType 
    transaction_amount: Decimal 
    created_at: datetime 

class DepositCreate(BaseModel):
    transaction_amount: Decimal = Field(gt=0)

class WithdrawalCreate(BaseModel):
    transaction_amount: Decimal = Field(gt=0)

class TransferCreate(BaseModel):
    receiver_account_number: str
    transaction_amount: Decimal = Field(gt=0)