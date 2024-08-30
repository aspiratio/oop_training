from flask import (
    flash,
    render_template,
    request,
)
from sqlmodel import Session

from app.db import create_session, get_engine
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash

from app.models.user import User
from app.views.base_view import BaseView


class AuthView(BaseView):
    def register_routes(self):
        @self.blueprint.route("/register", methods=("GET", "POST"))
        def register():
            if request.method == "POST":
                username = request.form["username"]
                password = request.form["password"]
                is_admin = int(
                    request.form.get("is_admin", "0")
                )  # フォームから is_admin が渡されれば 1、なければ 0

                error = None

                if not username:
                    error = "ユーザーネームは必須です"
                elif not password:
                    error = "パスワードは必須です"

                if error is None:
                    try:
                        with create_session() as session:
                            user = User(
                                name=username,
                                password=generate_password_hash(password),
                                is_admin=is_admin,
                            )
                            session.add(user)
                            session.commit()
                    except (
                        IntegrityError
                    ):  # DBの整合性が取れていない時に出る例外のみをキャッチ
                        error = f"ユーザー {username} は既に登録されています"
                    else:
                        return self.redirect_to("auth.login")

                flash(error)
            return render_template("auth/register.html")

        @self.blueprint.route("/login", methods=("GET", "POST"))
        def login():
            if request.method == "POST":
                return
            return render_template("auth/login.html")
