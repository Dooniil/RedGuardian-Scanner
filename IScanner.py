from abc import ABC, abstractmethod


class IScanner(ABC):
    @staticmethod
    @abstractmethod
    def scan(body: dict) -> any:
        pass
