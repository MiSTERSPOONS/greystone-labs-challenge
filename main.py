from fastapi import FastAPI
from src.sqlmodel.models.user import User
from src.db import create_db_and_tables, session
from src.routers.loans import loan_router

app = FastAPI()

@app.get("/")
def read_root():
    return "Welcome to the Greystone Loan Amortization App"

app.include_router(loan_router)

# User Routes
@app.post("/signup", response_model=User)
def signup(user: User):
    with session:
        session.add(user)
        session.commit()
        session.refresh(user)
    return user

if __name__ == "__main__":
    create_db_and_tables()