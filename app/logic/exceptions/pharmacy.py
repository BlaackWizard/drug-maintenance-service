from dataclasses import dataclass

from .base import LogicException


@dataclass(eq=False)
class PharmacyByTitleAlreadyExistsException(LogicException):
    title: str

    @property
    def message(self):
        return f'Аптека с таким названием уже существует "{self.title}"'


@dataclass(eq=False)
class PharmacyOrProductNotExistsException(LogicException):

    @property
    def message(self):
        return 'Не удалось найти товар или аптеку, проверьте ввели вы правильно id товара и аптеки.'


@dataclass(eq=False)
class PharmacyNotFoundException(LogicException):

    @property
    def message(self):
        return 'Аптека не найдена'