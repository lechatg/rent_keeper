from typing import Literal, Self
from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, Field, model_validator
from enum import Enum
from datetime import date


class OperationType(str, Enum):
    income = 'Income'
    expense = 'Expense'


class SourceType(str, Enum):
    direct = 'Direct'
    aggregator = 'Aggregator'
    website = 'Website'


class OperationIn(BaseModel):
    type_operation: OperationType
    date_of_payment: date
    extra_info: str | None = None


class ExpenseIn(OperationIn):
    type_operation: Literal[OperationType.expense]
    total_expense: int = Field(ge=0)


class ExpenseInWithUser(ExpenseIn):
    user_id: int


class IncomeIn(OperationIn):
    type_operation: Literal[OperationType.income]
    gross_income: int = Field(ge=0)
    comission: int = Field(ge=0)
    revenue_after_comission: int = Field(ge=0)
    date_in: date
    date_out: date
    fullname: str | None = Field(max_length=100)
    phone: str | None = Field(max_length=20)
    source: SourceType

    @model_validator(mode='after')
    def validate_dates(self) -> Self:
        if self.date_out <= self.date_in:
            raise HTTPException(status_code=400, detail='date_out must be later than date_in')
        return self


class IncomeInWithUser(IncomeIn):
    user_id: int


class OperationCreated(BaseModel):
    ok: bool = True
    id: int

class ExpenseOut(ExpenseInWithUser):
    id: int

    model_config = {
        "from_attributes": True
    }


class IncomeOut(IncomeInWithUser):
    id: int

    model_config = {
        "from_attributes": True
    }


class OperationDeleted(OperationCreated):
    pass

class OperationUpdated(OperationCreated):
    updated: bool = True
