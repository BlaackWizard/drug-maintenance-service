from dataclasses import dataclass

from ...domain.events.base import BaseEvent
from ...domain.values.product import Text, Title


@dataclass
class NewPharmacyCreatedEvent(BaseEvent):
    pharmacy_oid: str
    title: Title
    description: Text
