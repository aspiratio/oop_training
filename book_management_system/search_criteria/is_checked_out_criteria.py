from search_criteria.search_criteria import SearchCriteria


class ExactMatchIsCheckedOutSearchCriteria(SearchCriteria):
    def __init__(self, is_checked_out: bool):
        self._is_checked_out = is_checked_out

    def to_sql(self) -> str:
        return "is_checked_out = ?"

    def get_params(self) -> list:
        return [self._is_checked_out]
