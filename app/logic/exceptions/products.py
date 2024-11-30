from dataclasses import dataclass

from .base import LogicException


@dataclass(eq=False)
class ProductWithThatTitleAlreadyExistsException(LogicException):
    title: str

    @property
    def message(self):
        return f'Товар "{self.title}" уже существует.'


@dataclass(eq=False)
class ProductExpiresDateException(LogicException):

    @property
    def message(self):
        return 'Товар уже просрочен!'


@dataclass(eq=False)
class ProductNotFoundException(LogicException):

    @property
    def message(self):
        return 'Товар не найден'
