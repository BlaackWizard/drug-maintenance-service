from dataclasses import dataclass

from app.domain.events.base import BaseEvent
from app.domain.values.product import Title, Text


@dataclass
class NewPharmacyCreatedEvent(BaseEvent):
    pharmacy_oid: str
    title: Title
    description: Text
