from typing import Annotated, List
from fastapi import APIRouter, Request, Query
from sqlmodel import Session, select, col
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
@loan_router.get("/all/", response_model=List[Loan])
async def fetch_all_user_loans(
    user_id: int
):
    with Session(engine) as session:
        statement = select(Loan).where(col(Loan.user_id) == user_id)
        results = session.exec(statement).all()
        return results
# Share loan with another user