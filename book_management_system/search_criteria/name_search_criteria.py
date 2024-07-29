from search_criteria import SearchCriteria


class LikeNameSearchCriteria(SearchCriteria):
    def __init__(self, name: str):
        if len(name) == 0:
            raise ValueError("名前を指定してください")
        self._name = name

    def to_sql(self) -> str:
        return f"genre = '{self._genre}'"
