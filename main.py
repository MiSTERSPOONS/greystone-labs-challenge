from fastapi import FastAPI, HTTPException, status
from sqlmodel import Session, select, col
from src.sqlmodel.models.user import User
from src.db.initialize import create_db_and_tables, engine
from src.routers.loans import loan_router

create_db_and_tables()
app = FastAPI()

@app.get("/")
def read_root():
    return "Welcome to the Greystone Loan Amortization App"

app.include_router(loan_router)

# User Routes
@app.post("/signup", response_model=User)
def signup(user: User):
    with Session(engine) as session:
        statement = select(User).where(User.email == user.email)
        results = session.exec(statement).all()

        if results:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists") 

        session.add(user)
        session.commit()
        session.refresh(user)
        return user
