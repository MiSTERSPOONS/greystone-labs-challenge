from sqlmodel import SQLModel, Session, create_engine

engine = create_engine("sqlite:///database.db")
session = Session(engine)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)