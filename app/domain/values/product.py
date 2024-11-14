from datetime import datetime

from .base import BaseValueObject, VT
from dataclasses import dataclass

from ..exceptions.product import EmptyTextException, TitleTooLongException, ExpiresDateException


@dataclass(frozen=True)
class Text(BaseValueObject):
    value: str

    def validate(self):
        if not self.value:
            raise EmptyTextException()

    def as_generic_type(self) -> VT:
        return str(self.value)


@dataclass(frozen=True)
class Title(BaseValueObject):
    value: str

    def validate(self):
        if not self.value:
            raise EmptyTextException()

        if len(self.value) > 255:
            raise TitleTooLongException(self.value)

    def as_generic_type(self) -> VT:
        return str(self.value)


@dataclass(frozen=True)
class ExpiresDate(BaseValueObject):
    value: datetime

    def validate(self):
        if datetime.now() > self.value:
            raise ExpiresDateException()

    def as_generic_type(self) -> VT:
        return self.value

