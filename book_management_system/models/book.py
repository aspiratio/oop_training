# 値オブジェクト
class BookName:
    def __init__(self, value: str) -> None:
        if len(value) == 0:
            raise ValueError("名前を入力してください")
        if len(value) > 10:
            raise ValueError("名前は10文字以内です")
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
        # Memo: Bookクラスと変わらないが、未登録の本のみを指定するメソッドを作るためにサブクラスを定義する
        super().__init__(name, genre)
