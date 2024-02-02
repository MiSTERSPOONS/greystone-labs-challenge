from typing import Optional
from decimal import Decimal
from sqlmodel import Field, SQLModel

class Loan(SQLModel, table=True):
    loan_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.user_id")
    loan_amount: Decimal = Field(default=0, decimal_places=2)
    annual_interest_rate: Decimal = Field(default=None, decimal_places=2)
    loan_term_months: int