from typing import Optional
from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    email: str
    password: str