from decimal import Decimal
from sqlmodel import SQLModel

class LoanSchedule(SQLModel):
    month: int
    remaining_balance: Decimal
    monthly_payment: Decimal