from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class BaseEntity(ABC):
    id: int # noqa
    created_at: datetime = field(
        default_factory=lambda: datetime.now(),
        kw_only=True,
    )

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, __value: 'BaseEntity') -> bool:
        return self.id == __value.id
