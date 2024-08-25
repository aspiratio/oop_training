import click
from flask import current_app
from sqlmodel import SQLModel, create_engine
from .models import *


def init_db():
    database_url = current_app.config["DATABASE_URL"]
    engine = create_engine(database_url, echo=True)
    SQLModel.metadata.create_all(engine)  # models で定義したテーブルを作る


# 以下、flask --app app init-db のコマンドで init_db を実行できるようにするための記述
@click.command("init-db")
def init_db_command():
    init_db()
    click.echo("データベースを初期化しました")


def init_app(app):
    app.cli.add_command(init_db_command)
