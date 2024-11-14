from dataclasses import dataclass
from .base import ApplicationException


@dataclass(eq=False)
class TitleTooLongException(ApplicationException):
    text: str

    @property
    def message(self):
        return f'The text is too long "{self.text[:255]}"'


@dataclass(eq=False)
class EmptyTextException(ApplicationException):
    @property
    def message(self):
        return 'Text cannot be empty'


@dataclass(eq=False)
class ExpiresDateException(ApplicationException):
    @property
    def message(self):
        return f'The expiration date has expired'

