from decimal import Decimal
import uuid
from datetime import date, datetime, timezone
import sqlalchemy.dialects.postgresql as pg
from enum import Enum
from sqlmodel import Column, Field, SQLModel

class UserModel(SQLModel, table= True):
    __tablename__= 'users'
    user_id: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    name: str
    email: str = Field(
    sa_column=Column(
        pg.VARCHAR,
        nullable=False,
        unique=True,
        index=True,
    )
)   
    dob: date = Field(sa_column=Column(pg.DATE, nullable=False))
    is_admin: bool = Field(default=False, sa_column=Column(pg.BOOLEAN, nullable=False, default=False))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc)))

class StatusType(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    FROZEN = "frozen" 
    CLOSED = "closed"

class AccountModel(SQLModel, table= True):
    __tablename__= 'accounts'
    account_id: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    account_number: str = Field(
            sa_column=Column(
                pg.VARCHAR(12),
                nullable=False,
                unique=True,
                index=True,
            )
        )
    user_id: uuid.UUID = Field(foreign_key="users.user_id",nullable=False, unique=True, index=True)
    balance: Decimal = Field(default=Decimal("0.00"), sa_column=Column(pg.NUMERIC(12, 2), nullable=False))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc)))
    status: StatusType = Field(default=StatusType.ACTIVE, sa_column=Column(pg.VARCHAR(10), nullable=False, default=StatusType.ACTIVE))

class TransactionType(str, Enum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    TRANSFER = "transfer"
    SENT = "sent"

class TransactionModel(SQLModel, table= True):
    __tablename__= 'transactions'
    transaction_id: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    sender_account_number: str | None = Field(default=None, foreign_key="accounts.account_number", nullable=True)
    receiver_account_number: str | None = Field(default=None, foreign_key="accounts.account_number", nullable=True)
    transaction_type: TransactionType = Field(sa_column=Column(pg.VARCHAR(10), nullable=False))
    transaction_amount: Decimal = Field(sa_column=Column(pg.NUMERIC(12, 2), nullable=False))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc)))