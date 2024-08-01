from search_criteria.search_criteria import SearchCriteria


class ExactMatchGenreSearchCriteria(SearchCriteria):
    def __init__(self, genre: str):
        if len(genre) == 0:
            raise ValueError("ジャンルを指定してください")
        self._genre = genre

    def to_sql(self) -> str:
        return "genre = ?"

    def get_params(self) -> list:
        return [self._genre]
