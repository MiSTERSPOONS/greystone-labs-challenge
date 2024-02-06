from typing import Optional
from sqlmodel import Field, SQLModel

class LoanShare(SQLModel, table=True):
    loan_share_id: Optional[int] = Field(default=None, primary_key=True)
    source_user_id: int = Field(default=None, foreign_key="user.user_id")
    target_user_id: int = Field(default=None, foreign_key="user.user_id")
    loan_id: int = Field(default=None, foreign_key="loan.loan_id")