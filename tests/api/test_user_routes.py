from fastapi.testclient import TestClient
from sqlmodel import Session, col, select
from main import app
from src.db.initialize import engine
from src.sqlmodel.models.user import User

client = TestClient(app)

def test_server():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == "Welcome to the Greystone Loan Amortization App"


def test_user_signup():
    response = client.post(
        "/signup/",
        json={
            "user_id": 101,
            "first_name": "John",
            "last_name": "Wick",
            "email": "johnwick1@gmail.com",
            "password": "123"
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "last_name": "Wick",
        "first_name": "John",
        "email": "johnwick1@gmail.com",
        "user_id": 101,
        "password": "123"
    }
    # The test creates an actual user inside our SQLite DB, so removing user after running test
    # Would not do this in real application
    with Session(engine) as session:
        statement = select(User).where(col(User.email) == "johnwick1@gmail.com")
        results = session.exec(statement)

        user = results.one()

        session.delete(user)  
        session.commit()


def test_signup_existing_user():
    # Create a user first
    response = client.post(
        "/signup/",
        json={
            "user_id": 101,
            "first_name": "John",
            "last_name": "Wick",
            "email": "johnwick1@gmail.com",
            "password": "123"
        },
    )
    # Create a user with same info
    assert response.status_code == 200
    response = client.post(
        "/signup/",
        json={
            "user_id": 101,
            "first_name": "John",
            "last_name": "Wick",
            "email": "johnwick1@gmail.com",
            "password": "123"
        },
    )
    assert response.status_code == 409
    assert response.json() == {"detail": "User already exists"}

    # The test creates an actual user inside our SQLite DB, so removing user after running test
    # Would not do this in real application
    with Session(engine) as session:
        statement = select(User).where(col(User.email) == "johnwick1@gmail.com")
        results = session.exec(statement)

        user = results.one()

        session.delete(user)  
        session.commit()