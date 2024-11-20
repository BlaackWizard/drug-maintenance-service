from dataclasses import dataclass
from datetime import datetime

from ..exceptions.product import (EmptyTextException, ExpiresDateException,
                                  PriceIsNegativeValueException,
                                  TitleTooLongException)
from .base import VT, BaseValueObject


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

        if len(str(self.value)) > 255:
            raise TitleTooLongException(self.value)

    def as_generic_type(self) -> VT:
        return str(self.value)


@dataclass(frozen=True)
class ExpiresDate(BaseValueObject):
    value: datetime

    def validate(self):
        if self.value < datetime.now():
            raise ExpiresDateException

    def as_generic_type(self) -> VT:
        return self.value


@dataclass(frozen=True)
class Price(BaseValueObject):
    value: float

    def validate(self):
        if self.value < 0:
            raise PriceIsNegativeValueException

    def as_generic_type(self) -> VT:
        return float(self.value)
