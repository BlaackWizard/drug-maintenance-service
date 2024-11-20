from dataclasses import dataclass

from ...domain.entities.base import BaseEntity
from ...domain.values.product import Price


@dataclass
class PriceEntity(BaseEntity):
    product: 'ProductEntity' # noqa
    pharmacy: 'PharmacyEntity' # noqa
    price: Price

    def __hash__(self) -> int:
        return hash(self.oid)
