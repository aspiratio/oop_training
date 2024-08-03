from models.user import (
    AdminUserApplicationService,
    GeneralUserApplicationService,
    UserApplicationService,
)
from repository.book_repository import SQLiteBookRepository
from models.book import BookName
from repository.sqlite_connection_manager import SQLiteConnectionManager
from search_criteria.genre_search_criteria import ExactMatchGenreSearchCriteria


def main():
    connection_manager = SQLiteConnectionManager("book_management.db")
    repo = SQLiteBookRepository(connection_manager)
    admin_user_application_service = AdminUserApplicationService(repo)
    general_user_application_service = GeneralUserApplicationService(repo)

    # register(admin_user_application_service)
    # search(general_user_application_service)
    # delete(admin_user_application_service)
    rent(general_user_application_service)
    # return_(general_user_application_service)


def register(admin_user_application_service: AdminUserApplicationService):
    admin_user_application_service.register_book(
        BookName("スッキリわかるJAVA入門"), "技術書"
    )
    admin_user_application_service.register_book(
        BookName("入社1年目の教科書"), "ビジネス書"
    )
    admin_user_application_service.register_book(
        BookName("ビジョナリー・カンパニー①"), "ビジネス書"
    )
    admin_user_application_service.register_book(
        BookName("ビジョナリー・カンパニー②"), "ビジネス書"
    )
    admin_user_application_service.register_book(BookName("リーダブルコード"), "技術書")


def search(user_application_service: UserApplicationService):
    criteria = ExactMatchGenreSearchCriteria("ビジネス書")
    user_application_service.search_books([criteria])


def delete(admin_user_application_service: AdminUserApplicationService):
    admin_user_application_service.deregister_book(10)


def rent(general_user_application_service: GeneralUserApplicationService):
    general_user_application_service.rent_book(17)


def return_(general_user_application_service: GeneralUserApplicationService):
    general_user_application_service.return_book(17)


if __name__ == "__main__":
    main()
