from abc import ABC, abstractmethod


class SearchCriteria(ABC):
    @abstractmethod
    def to_sql(self) -> str:
        pass
