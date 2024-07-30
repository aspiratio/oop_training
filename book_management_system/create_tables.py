import sqlite3


def read_query(file_path: str) -> str:
    with open(file_path, "r") as file:
        return file.read()


def create_table(dbname: str, books_query_file: str, users_query_file: str):
    # DBへの接続処理
    connection = sqlite3.connect(dbname)
    cursor = connection.cursor()

    # クエリの読み込み
    books_query = read_query(books_query_file)
    users_query = read_query(users_query_file)

    # テーブル作成
    cursor.execute(books_query)
    cursor.execute(users_query)
    connection.commit()

    # DBへの接続切断
    connection.close()


if __name__ == "__main__":
    dbname = "book_management.db"
    books_query_file = "queries/create_books.sql"
    users_query_file = "queries/create_users.sql"
    create_table(dbname, books_query_file, users_query_file)
    print("テーブルを作成しました")
