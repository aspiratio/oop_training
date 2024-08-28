from sqlmodel import Field, SQLModel
from flask_login import UserMixin


class User(UserMixin, SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    password: str
    is_admin: int
