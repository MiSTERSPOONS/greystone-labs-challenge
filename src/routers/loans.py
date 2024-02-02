from fastapi import APIRouter
from src.sqlmodel.models.loan import Loan
from src.db import session

loan_router = APIRouter(
    prefix="/loans",
    tags=["loans"]
)

# Create a loan
@loan_router.post("/create")
def create_loan(loan: Loan):
    session.add(loan)
    session.commit()
    session.refresh()
    return loan

# Fetch a loan schedule
# Fetch a loan summary for a specific month
# Fetch all loans for a user
# Share loan with another user