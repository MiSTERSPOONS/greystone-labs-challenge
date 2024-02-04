from decimal import Decimal
from sqlmodel import SQLModel

class LoanSummary(SQLModel):
    principal_balance: Decimal
    amount_principal_paid: Decimal
    amount_interest_paid: Decimal