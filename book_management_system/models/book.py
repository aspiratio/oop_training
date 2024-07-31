# 値オブジェクト
class BookName:
    def __init__(self, value: str) -> None:
        if len(value) == 0:
            raise ValueError("名前を入力してください")
        if len(value) > 20:
            raise ValueError("名前は20文字以内です")
        self.value = value

    def __str__(self):
        return self.value


# メインで使用するクラス
class Book:
    def __init__(self, name: BookName, genre: str) -> None:
        self._name = name
        self._genre = genre

    @property
    def name(self) -> BookName:
        return self._name

    @property
    def genre(self) -> str:
        return self._genre


class RegisteredBook(Book):
    def __init__(self, name: BookName, genre: str, is_checked_out: bool) -> None:
        super().__init__(name, genre)
        self.is_checked_out = is_checked_out


class UnregisteredBook(Book):
    def __init__(self, name: BookName, genre: str) -> None:
        super().__init__(name, genre)
        self._is_checked_out = False

    @property
    def is_checked_out(
        self,
    ):  # 登録前の本は貸出されることがないため、外から変更できないようにする
        return self._is_checked_out
