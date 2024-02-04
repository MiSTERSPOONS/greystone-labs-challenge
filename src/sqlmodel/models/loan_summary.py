from decimal import Decimal
from sqlmodel import SQLModel

class LoanSummary(SQLModel):
    principal_balance: Decimal
    total_principal_paid: Decimal
    total_interest_paid: Decimal