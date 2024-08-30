import os

from flask import Flask
from flask_login import LoginManager

from app.models.user import User


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE_URL=f"sqlite:///{os.path.join(app.instance_path, 'library.sqlite')}",
    )

    # LoginManager を初期化
    login_manager = LoginManager()
    login_manager.init_app(app)

    # 未ログインのユーザーが login_required のページにアクセスしようとした場合のリダイレクト先
    login_manager.login_view = "auth.login"

    # ログインユーザーを取得するためのコールバック関数
    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id)  # ここでユーザーをDBから取得する

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db

    db.init_app(app)

    from .views.auth import AuthView

    auth_view = AuthView("auth", "/auth")
    app.register_blueprint(auth_view.blueprint)

    return app
