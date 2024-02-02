from fastapi import APIRouter
from sqlmodel import Session
from src.db.initialize import engine
from src.sqlmodel.models.loan import Loan

loan_router = APIRouter(
    prefix="/loans",
    tags=["loans"]
)

# Create a loan
@loan_router.post("/create/", response_model=Loan)
def create_loan(loan: Loan):
    with Session(engine) as session:
        session.add(loan)
        session.commit()
        session.refresh(loan)
        return loan

# Fetch a loan schedule
# Fetch a loan summary for a specific month
# Fetch all loans for a user
# Share loan with another user