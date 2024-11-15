import uuid
from abc import ABC
from dataclasses import dataclass, field
from uuid import UUID


@dataclass
class BaseEvent(ABC):
    event_id: UUID = field(default_factory=uuid.uuid4, kw_only=True)
