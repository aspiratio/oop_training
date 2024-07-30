from book_management_system.search_criteria.search_criteria import SearchCriteria


class ExactMatchIsCheckedOutSearchCriteria(SearchCriteria):
    def __init__(self, is_checked_out: bool):
        self._is_checked_out = is_checked_out

    def to_sql(self) -> str:
        return f"is_checked_out = {self._is_checked_out}"
