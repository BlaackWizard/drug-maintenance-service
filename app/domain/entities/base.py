from abc import ABC
from copy import copy
from dataclasses import dataclass, field
from datetime import datetime

from app.domain.events.base import BaseEvent


@dataclass
class BaseEntity(ABC):
    id: int # noqa
    created_at: datetime = field(
        default_factory=lambda: datetime.now(),
        kw_only=True,
    )
    _events: list[BaseEvent] = field(
        default_factory=list,
        kw_only=True,
    )

    def register_event(self, event: BaseEvent) -> None:
        self._events.append(event)

    def pull_requests(self) -> list[BaseEvent]:
        registered_events = copy(self._events)
        self._events.clear()
        return registered_events

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, __value: 'BaseEntity') -> bool:
        return self.id == __value.id
