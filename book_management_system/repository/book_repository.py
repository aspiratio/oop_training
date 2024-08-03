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
    def search(
        self, criteria: list[SearchCriteria], limit: int
    ) -> list[RegisteredBook]:
        pass

    @abstractmethod
    def add(self, book: UnregisteredBook) -> None:
        pass

    @abstractmethod
    def delete(self, book_id: int) -> int:
        pass

    @abstractmethod
    def update(self, book_id: int, column: str, new_value: any) -> int:
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

    def _create_where_statement(self, criteria: list[SearchCriteria]) -> str:
        where_clauses = [criterion.to_sql() for criterion in criteria]
        return " AND ".join(where_clauses)

    def _create_placeholder_params(
        self, criteria: list[SearchCriteria], limit: int
    ) -> list:
        params = []
        for criterion in criteria:
            param = criterion.get_params()
            params.extend(param)  # プレースホルダーに入れる値を一つのリストにする

        params.append(int(limit))  # LIMITをパラメータとして追加
        return params

    def search(
        self, criteria: list[SearchCriteria], limit: int = 100
    ) -> list[RegisteredBook]:
        if len(criteria) != 0:
            where_statement = self._create_where_statement(criteria)
        else:
            where_statement = "1 = 1"
        params = self._create_placeholder_params(criteria, limit)

        query = f"SELECT name, genre, is_checked_out FROM books WHERE {where_statement} ORDER BY genre, name LIMIT ?"

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

    def delete(self, book_id: int) -> int:
        query = f"DELETE FROM books WHERE id = ?"

        with self._connection_manager as connection:
            cursor = connection.cursor()
            cursor.execute(
                query,
                [book_id],
            )
            connection.commit()
            return cursor.rowcount

    def update(self, book_id: int, column: str, new_value: any) -> int:
        # データベースからカラム名を取得
        with self._connection_manager as connection:
            cursor = connection.cursor()
            cursor.execute("PRAGMA table_info(books)")
            columns_info = cursor.fetchall()
            allowed_columns = {info[1] for info in columns_info}

        # SQLインジェクション対策：テーブルに存在するカラム以外が渡されたらエラーにする
        if column not in allowed_columns:
            raise ValueError(f"存在しないカラムが指定されました: {column}")

        # 元の値を取得
        with self._connection_manager as connection:
            query_select = f"SELECT {column} FROM books WHERE id = ?"
            cursor = connection.cursor()
            cursor.execute(query_select, [book_id])
            original_value = cursor.fetchone()[0]

        # 元の値と新しい値が同じなら更新をスキップ
        if original_value == new_value:
            return 0

        query = f"UPDATE books SET {column} = ? WHERE id = ?"

        with self._connection_manager as connection:
            cursor = connection.cursor()
            cursor.execute(query, [new_value, book_id])
            connection.commit()
            return cursor.rowcount
