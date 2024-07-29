from abc import ABC, abstractmethod
from book_management_system.models.book import RegisteredBook

from book_management_system.search_criteria.search_criteria import SearchCriteria


class BookRepository(ABC):
    @abstractmethod
    def search(self, criteria: SearchCriteria) -> list[RegisteredBook]:
        pass


class SQLiteBookRepository(BookRepository):
    def search(self, criteria: list[SearchCriteria]) -> list[RegisteredBook]:
        # データベースに接続する処理
        where_clauses = [criteria.to_sql() for criterion in criteria]
        where_statement = "AND".join(where_clauses)
        query = f"SELECT * FROM WHERE {where_statement}"
        # データベースの接続を切る処理
