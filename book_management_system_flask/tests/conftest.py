import os
import tempfile

import pytest
from app import create_app
from app.db import get_engine, init_db
from sqlmodel import Session
from app.models import *


def _add_mock_data():
    engine = get_engine()
    with Session(engine) as session:
        mock_data = [
            User(name="太郎", password="password", is_admin=0),
            User(name="サトシ", password="password", is_admin=1),
            Book(name="スッキリわかるJAVA入門", genre="技術書"),
            Book(name="ハンターハンター", genre="マンガ"),
            Loan(
                book_id=1,
                user_id=1,
                loan_date="2024-08-01",
                return_due_date="2024-09-01",
            ),
            Loan(
                book_id=2,
                user_id=2,
                loan_date="2024-08-02",
                return_due_date="2024-09-02",
                return_date="2024-08-10",
            ),
        ]
        session.add_all(mock_data)
        session.commit()


@pytest.fixture
def test_app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({"TESTING": True, "DATABASE_URL": db_path})

    with app.app_context():
        init_db()
        _add_mock_data()

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def test_client(app):
    return app.test_client()
