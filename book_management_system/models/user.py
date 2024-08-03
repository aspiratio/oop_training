from models.book import BookName, RegisteredBook, UnregisteredBook
from repository.book_repository import BookRepository
from search_criteria.search_criteria import SearchCriteria


# 値オブジェクト
class UserId:
    def __init__(self, value: str) -> None:
        if len(value) == 0:
            raise ValueError("idを入力してください")
        if len(value) > 5:
            raise ValueError("idは5文字以内です")


class UserName:
    def __init__(self, value: str) -> None:
        if len(value) == 0:
            raise ValueError("名前を入力してください")
        if len(value) > 10:
            raise ValueError("名前は10文字以内です")


# メインで使用するクラス
class User:
    def __init__(self, id: UserId, name: UserName, is_admin: bool) -> None:
        self._id = id
        self._name = name
        self._is_admin = is_admin

    @property
    def id(self) -> UserId:
        return self._id

    @property
    def name(self) -> UserName:
        return self._name


class UserApplicationService:
    def __init__(self, repository: BookRepository) -> None:
        self.repository = repository

    def search_books(self, criteria: list[SearchCriteria], limit: int = None) -> None:
        if limit:
            results = self.repository.search(criteria, limit)
        else:
            results = self.repository.search(criteria)

        for result in results:
            print(result.name, result.genre, result.is_checked_out)


class GeneralUserApplicationService(UserApplicationService):
    def rent_book(self, book_id: int) -> None:
        rowcount = self.repository.update(book_id, "is_checked_out", True)
        print(f"{rowcount}冊の本を貸出しました")

    def return_book(self, book: RegisteredBook) -> None:
        pass


class AdminUserApplicationService(UserApplicationService):
    def register_book(self, name: BookName, genre: str) -> None:
        book = UnregisteredBook(name, genre)
        self.repository.add(book)
        print(f"{name}を登録しました")

    def deregister_book(self, book_id: int) -> None:
        rowcount = self.repository.delete(book_id)
        print(f"{rowcount}冊の削除に成功しました")
