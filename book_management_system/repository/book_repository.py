from abc import ABC, abstractmethod
from book_management_system.models.book import (
    BookName,
    RegisteredBook,
    UnregisteredBook,
)
from book_management_system.repository.sqlite_connection_manager import (
    SQLiteConnectionManager,
)

from book_management_system.search_criteria.search_criteria import SearchCriteria


class BookRepository(ABC):
    @abstractmethod
    def search(self, criteria: SearchCriteria) -> list[RegisteredBook]:
        pass


class SQLiteBookRepository(BookRepository):
    def __init__(self, connection_manager: SQLiteConnectionManager) -> None:
        self._connection_manager = connection_manager

    def _row_to_registered_book(self, row: tuple) -> RegisteredBook:
        name, genre, is_checked_out = row
        book_name = BookName(name)
        return RegisteredBook(book_name, genre, is_checked_out)

    def search(self, criteria: list[SearchCriteria]) -> list[RegisteredBook]:
        where_clauses = [criterion.to_sql() for criterion in criteria]
        where_statement = "AND".join(where_clauses)
        query = f"SELECT name, genre, is_checked_out FROM books WHERE {where_statement} ORDER BY genre, name"

        with self._connection_manager as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            return self._row_to_registered_book(results)
