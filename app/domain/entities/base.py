from abc import ABC
from copy import copy
from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4

from ...domain.events.base import BaseEvent


@dataclass
class BaseEntity(ABC):
    oid: str = field(
        default_factory=lambda: str(uuid4()),
        kw_only=True,
    )
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
