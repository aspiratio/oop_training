import click
from flask import current_app, g
from sqlmodel import SQLModel, create_engine
from .models import *

def get_engine():
    if "engine" not in g:
        database_url = current_app.config["DATABASE_URL"]
        g.engine = create_engine(database_url, echo=True)
    return g.engine

def init_db():
    engine = get_engine()
    SQLModel.metadata.create_all(engine)  # models で定義したテーブルを作る


# 以下、flask --app app init-db のコマンドで init_db を実行できるようにするための記述
@click.command("init-db")
def init_db_command():
    init_db()
    click.echo("データベースを初期化しました")


def init_app(app):
    app.cli.add_command(init_db_command)

