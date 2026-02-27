from abc import ABC, abstractmethod


class Shape(ABC):

    @abstractmethod
    def area(self) -> float:
        pass

    @abstractmethod
    def perimeter(self) -> float:
        pass

    @abstractmethod
    def is_valid(self) -> bool:
        pass

    @property
    @abstractmethod
    def centroid(self):
        pass
