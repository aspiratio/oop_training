from sqlmodel import SQLModel, create_engine
from .models import *


def init_db(app):
    database_url = app.config["DATABASE_URL"]
    engine = create_engine(database_url, echo=True)
    SQLModel.metadata.create_all(engine)  # models で定義したテーブルを作る
