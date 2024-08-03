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

    @property
    def is_admin(self) -> bool:
        return self._is_admin


class UserApplicationService:
    def __init__(self, user: User, repository: BookRepository) -> None:
        self.user = user
        self.repository = repository

    def search_books(self, criteria: list[SearchCriteria], limit: int = None) -> None:
        if limit:
            results = self.repository.search(criteria, limit)
        else:
            results = self.repository.search(criteria)

        for result in results:
            print(result.name, result.genre, result.is_checked_out)


class GeneralUserApplicationService(UserApplicationService):
    def __init__(self, user: User, repository: BookRepository) -> None:
        if user.is_admin:
            raise PermissionError("管理者ユーザーは利用できません")
        super().__init__(user, repository)

    def rent_book(self, book_id: int) -> None:
        rowcount = self.repository.update(book_id, "is_checked_out", True)
        if rowcount == 0:
            raise RuntimeError("その本は貸出中です")
        print(f"{rowcount}冊の本を貸出しました")

    def return_book(self, book_id: int) -> None:
        rowcount = self.repository.update(book_id, "is_checked_out", False)
        if rowcount == 0:
            raise RuntimeError("その本は返却済みです")
        print(f"{rowcount}冊の本を返却しました")


class AdminUserApplicationService(UserApplicationService):
    def __init__(self, user: User, repository: BookRepository) -> None:
        if not user.is_admin:
            raise PermissionError("一般ユーザーは利用できません")
        super().__init__(user, repository)

    def register_book(self, name: BookName, genre: str) -> None:
        book = UnregisteredBook(name, genre)
        self.repository.add(book)
        print(f"{name}を登録しました")

    def deregister_book(self, book_id: int) -> None:
        rowcount = self.repository.delete(book_id)
        print(f"{rowcount}冊の削除に成功しました")
