from models.book import RegisteredBook, UnregisteredBook
from repository.book_repository import BookRepository
from search_criteria.search_criteria import SearchCriteria


# 値オブジェクト
class UserId:
    def __init__(self, value: str):
        if len(value) == 0:
            raise ValueError("idを入力してください")
        if len(value) > 5:
            raise ValueError("idは5文字以内です")


class UserName:
    def __init__(self, value: str):
        if len(value) == 0:
            raise ValueError("名前を入力してください")
        if len(value) > 10:
            raise ValueError("名前は10文字以内です")


# メインで使用するクラス
class User:
    def __init__(self, id: UserId, name: UserName, is_admin: bool):
        self._id = id
        self._name = name
        self._is_admin = is_admin

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name


class UserApplicationService:
    def __init__(self, repository: BookRepository):
        self.repository = repository

    def search_books(self, criteria: SearchCriteria):
        self.repository.search(criteria)


class GeneralUserApplicationService(UserApplicationService):
    def rent_book(self, book: RegisteredBook):
        pass

    def return_book(self, book: RegisteredBook):
        pass


class AdminUserApplicationService(UserApplicationService):
    def register_book(self, book: UnregisteredBook):
        pass

    def deregister_book(self, book: RegisteredBook):
        pass
