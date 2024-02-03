from typing import List
from fastapi import APIRouter
from sqlmodel import Session, select, col
from src.db.initialize import engine
from src.sqlmodel.models.loan import Loan
from src.sqlmodel.models.loan_schedule import LoanSchedule
from src.utils.loan_amortization_calculation import LoanAmortizationCalculator

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
@loan_router.get("/schedule/", response_model=List[LoanSchedule])
async def fetch_loan_schedule(
    loan_id: int
):
    with Session(engine) as session:
        statement = select(Loan).where(col(Loan.loan_id) == loan_id)
        results = session.exec(statement).all()
        loan = results[0]

        loan_schedule = LoanAmortizationCalculator.calculate_loan_schedule(
            loan.loan_amount,
            loan.loan_term_months,
            loan.annual_interest_rate
        )

        return loan_schedule

# Fetch a loan summary for a specific month
# Fetch all loans for a user
@loan_router.get("/all/", response_model=List[Loan])
async def fetch_all_user_loans(
    user_id: int
):
    with Session(engine) as session:
        statement = select(Loan).where(col(Loan.user_id) == user_id)
        results = session.exec(statement).all()
        return results
# Share loan with another user