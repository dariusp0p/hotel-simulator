from abc import ABC, abstractmethod



class BaseRepository(ABC):

    @abstractmethod
    def add(self, identifier, obj) -> None:
        pass

    @abstractmethod
    def get_all(self) -> dict:
        pass

    @abstractmethod
    def update(self, identifier: str, obj) -> None:
        pass

    @abstractmethod
    def remove(self, identifier: str):
        pass
