from dataclasses import dataclass

from app.domain.exceptions.base import ApplicationException


@dataclass
class LogicException(ApplicationException):
    @property
    def message(self):
        return 'В обработки запроса возникла ошибка'
