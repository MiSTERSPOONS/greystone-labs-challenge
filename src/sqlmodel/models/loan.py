from typing import Optional
from sqlmodel import Field, SQLModel

class Loan(SQLModel, table=True):
    loan_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.user_id")
    loan_amount: float
    annual_interest_rate: float
    loan_term_months: int