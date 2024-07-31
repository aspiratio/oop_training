from abc import ABC, abstractmethod
from models.book import (
    BookName,
    RegisteredBook,
    UnregisteredBook,
)
from repository.sqlite_connection_manager import (
    SQLiteConnectionManager,
)

from search_criteria.search_criteria import SearchCriteria


class BookRepository(ABC):
    @abstractmethod
    def search(self, criteria: list[SearchCriteria]) -> list[RegisteredBook]:
        pass

    @abstractmethod
    def add(self, book: UnregisteredBook) -> None:
        pass


class SQLiteBookRepository(BookRepository):
    def __init__(self, connection_manager: SQLiteConnectionManager) -> None:
        self._connection_manager = connection_manager

    def _row_to_registered_book(self, row: tuple) -> RegisteredBook:
        """
        SELECTしたレコードをRegisteredBookのインスタンスを作成する
        """
        name, genre, is_checked_out = row
        book_name = BookName(name)
        return RegisteredBook(book_name, genre, is_checked_out)

    def _unregistered_book_to_dict(self, unregistered_book: UnregisteredBook) -> dict:
        """
        UnregisteredBookインスタンスのプロパティとbooksテーブルのカラム名を対応させた辞書を作成する
        """
        name = unregistered_book.name.value
        genre = unregistered_book.genre
        is_checked_out = unregistered_book.is_checked_out
        return {"name": name, "genre": genre, "is_checked_out": is_checked_out}

    def search(self, criteria: list[SearchCriteria]) -> list[RegisteredBook]:
        where_clauses = [criterion.to_sql() for criterion in criteria]
        where_statement = "AND".join(where_clauses)
        query = f"SELECT name, genre, is_checked_out FROM books WHERE {where_statement} ORDER BY genre, name"

        params = []
        for criterion in criteria:
            param = criterion.get_params()
            params.extend(param)  # プレースホルダーに入れる値を一つのリストにする

        with self._connection_manager as connection:
            cursor = connection.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()
            return [self._row_to_registered_book(row) for row in results]

    def add(self, book: UnregisteredBook) -> None:
        book_dict = self._unregistered_book_to_dict(book)
        query = "INSERT INTO books(name, genre, is_checked_out) VALUES(:name, :genre, :is_checked_out)"

        with self._connection_manager as connection:
            cursor = connection.cursor()
            cursor.execute(query, book_dict)
            connection.commit()
