from fastapi.testclient import TestClient
from sqlmodel import Session, col, select
from main import app
from src.db.initialize import engine
from src.sqlmodel.models.loan import Loan
from src.sqlmodel.models.user import User

client = TestClient(app)

def test_loans_create():
    # Create a User
    response = client.post(
        "/signup/",
        json={
            "user_id": 1337,
            "first_name": "John",
            "last_name": "Wick",
            "email": "johnwick@gmail.com",
            "password": "123"
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "user_id": 1337,
        "first_name": "John",
        "last_name": "Wick",
        "email": "johnwick@gmail.com",
        "password": "123"
    }

    # Create a Loan
    response = client.post(
        "/loans/create/",
        json={
            "user_id": 1337,
            "loan_id": 999,
            "loan_amount": 30000.00,
            "annual_interest_rate": 3,
            "loan_term_months": 48
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "user_id": 1337,
        "loan_id": 999,
        "loan_amount": "30000.00",
        "annual_interest_rate": "3.00",
        "loan_term_months": 48
    }
    # The test creates an actual user & loan inside our SQLite DB, so removing loan after running test
    # Would not do this in real application
    with Session(engine) as session:
        user_statement = select(User).where(col(User.user_id) == 1337)
        user_results = session.exec(user_statement)

        loan_statement = select(Loan).where(col(Loan.loan_id) == 999)
        loan_results = session.exec(loan_statement)

        loan = loan_results.one()
        user = user_results.one()

        session.delete(user)  
        session.delete(loan)  
        session.commit()

def test_loans_create_non_existent_user():
    # Create a loan first
    response = client.post(
        "/loans/create/",
        json={
            "user_id": 1337,
            "loan_id": 999999,
            "loan_amount": 30000.00,
            "annual_interest_rate": 3,
            "loan_term_months": 48
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Cannot create Loan for non-existent user"}

def test_fetch_all_user_loans():
    response = client.get(
        "/loans/all/?user_id=109876654321",
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Cannot fetch all loans. User does not exist."}

def test_loans_schedule():
    # Create a User
    response = client.post(
        "/signup/",
        json={
            "user_id": 1337,
            "first_name": "John",
            "last_name": "Wick",
            "email": "johnwick@gmail.com",
            "password": "123"
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "user_id": 1337,
        "first_name": "John",
        "last_name": "Wick",
        "email": "johnwick@gmail.com",
        "password": "123"
    }

    # Create a Loan
    response = client.post(
        "/loans/create/",
        json={
            "user_id": 1337,
            "loan_id": 999999,
            "loan_amount": 30000.00,
            "annual_interest_rate": 3,
            "loan_term_months": 48
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "user_id": 1337,
        "loan_id": 999999,
        "loan_amount": "30000.00",
        "annual_interest_rate": "3.00",
        "loan_term_months": 48
    }

    # Fetch loan schedule for created loan
    response = client.get(
        "/loans/schedule/?loan_id=999999",
    )
    assert response.status_code == 200
    assert len(response.json())== 48

    # The test creates an actual user & loan inside our SQLite DB, so removing loan after running test
    # Would not do this in real application
    with Session(engine) as session:
        user_statement = select(User).where(col(User.user_id) == 1337)
        user_results = session.exec(user_statement)

        loan_statement = select(Loan).where(col(Loan.loan_id) == 999999)
        loan_results = session.exec(loan_statement)

        loan = loan_results.one()
        user = user_results.one()

        session.delete(user)  
        session.delete(loan)  
        session.commit()

def test_loans_schedule_non_existent_loan():
    # Fetch loan schedule for non-existent loan
    response = client.get(
        "/loans/schedule/?loan_id=1234567890",
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Loan schedule does not exist"}

def test_fetch_loan_summary():
    # Create a User
    response = client.post(
        "/signup/",
        json={
            "user_id": 1337,
            "first_name": "John",
            "last_name": "Wick",
            "email": "johnwick@gmail.com",
            "password": "123"
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "user_id": 1337,
        "first_name": "John",
        "last_name": "Wick",
        "email": "johnwick@gmail.com",
        "password": "123"
    }

    # Create a Loan
    response = client.post(
        "/loans/create/",
        json={
            "user_id": 1337,
            "loan_id": 999999,
            "loan_amount": 30000.00,
            "annual_interest_rate": 3,
            "loan_term_months": 48
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "user_id": 1337,
        "loan_id": 999999,
        "loan_amount": "30000.00",
        "annual_interest_rate": "3.00",
        "loan_term_months": 48
    }

    # Fetch a loan summary
    response = client.get(
        "/loans/summary/?loan_id=999999&month=2",
    )
    assert response.status_code == 200
    assert response.json() == {
        "current_principal_balance": 28820.47,
        "total_principal_paid": 1179.53,
        "total_interest_paid": 148.53
    }

    # The test creates an actual user & loan inside our SQLite DB, so removing loan after running test
    # Would not do this in real application
    with Session(engine) as session:
        user_statement = select(User).where(col(User.user_id) == 1337)
        user_results = session.exec(user_statement)

        loan_statement = select(Loan).where(col(Loan.loan_id) == 999999)
        loan_results = session.exec(loan_statement)

        loan = loan_results.one()
        user = user_results.one()

        session.delete(user)  
        session.delete(loan)  
        session.commit()