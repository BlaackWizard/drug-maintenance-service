from dataclasses import dataclass

from .base import LogicException


@dataclass(eq=False)
class PharmacyByTitleAlreadyExistsException(LogicException):
    title: str

    @property
    def message(self):
        return f'Аптека с таким названием уже существует "{self.title}"'
