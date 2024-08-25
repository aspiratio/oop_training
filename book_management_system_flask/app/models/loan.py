from datetime import date
from sqlmodel import Field, SQLModel


class Loan(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    book_id: int = Field(foreign_key="book.id")
    user_id: int = Field(foreign_key="user.id")
    loan_date: date
    return_due_date: date
    return_date: date | None = None
