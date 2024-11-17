from abc import ABC
from dataclasses import dataclass
from typing import Generic, TypeVar, Any

from app.domain.events.base import BaseEvent

ET = TypeVar("ET", bound=BaseEvent)
ER = TypeVar("ER", bound=Any)


@dataclass(frozen=True)
class EventHandler(ABC, Generic[ET, ER]):
    def handle(self, event: ET) -> ER:
        ...
