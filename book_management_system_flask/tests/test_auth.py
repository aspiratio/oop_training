import pytest
from sqlmodel import Session, select
from app.db import get_engine
from app.models.user import User


class TestAuthView:
    def test_register_success_admin_user(self, test_client):
        # 登録ページのGETリクエストが成功する
        assert test_client.get("/auth/register").status_code == 200
        
        # ユーザー登録フォームのPOSTリクエストが成功する
        response = test_client.post("/auth/register", data={"username": "admin_user", "password": "admin_password", "is_admin": "1"})
        
        # ログインページにリダイレクトする
        assert response.status_code == 302
        assert response.headers["Location"] == "/auth/login"
        
        # DBに新しいユーザーが登録されている
        engine = get_engine()
        with Session(engine) as session:
            statement = select(User).where(User.name == "admin_user")
            # one() は条件に合致するレコードが1件でないとエラーになる https://sqlmodel.tiangolo.com/tutorial/one/#exactly-one
            user = session.exec(statement).one()
            assert user.is_admin == 1
        
    def test_register_success_general_user(self, test_client):
        # ユーザー登録フォームのPOSTリクエストが is_admin を含まずに成功する
        response = test_client.post("/auth/register", data={"username": "general_user", "password": "new_password"})
        
        # ログインページにリダイレクトする
        assert response.status_code == 302
        assert response.headers["Location"] == "/auth/login"
        
        # DBに新しいユーザーが登録されている
        engine = get_engine()
        with Session(engine) as session:
            statement = select(User).where(User.name == "general_user")
            # one() は条件に合致するレコードが1件でないとエラーになる https://sqlmodel.tiangolo.com/tutorial/one/#exactly-one
            user = session.exec(statement).one()
            assert user.is_admin == 0
    
    
    @pytest.mark.parametrize(
        {"username", "password", "message"},
        {
            ("", "", "ユーザーネームは必須です"),
            ("a", "", "パスワードは必須です"),
            ("太郎", "aaa", "ユーザー 太郎 は既に登録されています"),
        }
    )
    def test_register_validate_error(self, test_client, username, password, message):
        response = test_client.post("/auth/register", data={"username": username, "password": password})
        # エラーメッセージが返却されている
        assert message in response.get_data(as_text=True)
