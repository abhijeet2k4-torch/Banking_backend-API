from typing import Optional
from pydantic import BaseModel, ConfigDict
import uuid
from datetime import date, datetime

class UserModel(BaseModel):
    user_id: uuid.UUID
    name: str
    email: str
    dob: date
    is_admin: bool
    created_at: datetime

class UserCreateModel(BaseModel):
    name: str
    email: str
    dob: date

class PatchUserModel(BaseModel):
    model_config = ConfigDict(extra="forbid") 
    name: Optional[str] = None
    email: Optional[str] = None
    