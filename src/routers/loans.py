from typing import List
from fastapi import APIRouter, HTTPException, status
from sqlmodel import Session, select, col
from src.db.initialize import engine
from src.sqlmodel.models.loan import Loan
from src.sqlmodel.models.loan_schedule import LoanSchedule
from src.sqlmodel.models.loan_share import LoanShare
from src.sqlmodel.models.user import User
from src.utils.loan_amortization_calculation import LoanAmortizationCalculator

loan_router = APIRouter(
    prefix="/loans",
    tags=["loans"]
)

# Create a loan
@loan_router.post("/create/", response_model=Loan)
def create_loan(loan: Loan):
    with Session(engine) as session:
        statement = select(User).where(col(User.user_id) == loan.user_id)
        results = session.exec(statement).all()

        if not results:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cannot create Loan for non-existent user") 

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

        if not results:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Loan schedule does not exist") 

        loan = results[0]

        loan_schedule = LoanAmortizationCalculator.calculate_loan_schedule(
            loan.loan_amount,
            loan.loan_term_months,
            loan.annual_interest_rate
        )

        return loan_schedule

# Fetch a loan summary for a specific month
@loan_router.get('/summary/')
def fetch_loan_summary(
    loan_id: int,
    month: int
):
    with Session(engine) as session:
        statement = select(Loan).where(col(Loan.loan_id) == loan_id)
        results = session.exec(statement).all()

        if not results:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Loan summary does not exist") 

        loan = results[0]

        loan_schedule = LoanAmortizationCalculator.calculate_loan_schedule(
            loan.loan_amount,
            loan.loan_term_months,
            loan.annual_interest_rate
        )

        if month-1 < 0 or month > len(loan_schedule):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Loan summary for month: {month} does not exist") 

        loan_schedule_for_given_month = loan_schedule[month-1]

        loan_summary = LoanAmortizationCalculator.calculate_loan_summary(
            loan.loan_amount,
            loan_schedule_for_given_month
        )

        return loan_summary

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
@loan_router.post("/share/", response_model=LoanShare)
async def create_share_loan(
    loan_share: LoanShare
):
    if loan_share.source_user_id == loan_share.target_user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Cannot share loan. Source and Target user are the same.") 

    with Session(engine) as session:
        source_user_statement = select(User).where(col(User.user_id) == loan_share.source_user_id)
        results = session.exec(source_user_statement).all()

        if not results:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Cannot share loan. Source user does not exist.") 

        target_user_statement = select(User).where(col(User.user_id) == loan_share.target_user_id)
        results = session.exec(target_user_statement).all()

        if not results:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Cannot share loan. Target user does not exist.") 
        
        loan_statement = select(LoanShare).where(col(Loan.loan_id) == loan_share.loan_id)
        results = session.exec(loan_statement).all()

        if results:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Duplicate loan found. Source and Target Users are already sharing this loan")

        session.add(loan_share)
        session.commit()
        session.refresh(loan_share)
        return loan_share