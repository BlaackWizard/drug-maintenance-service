from dataclasses import dataclass

from ..values.product import ExpiresDate, Text, Title
from .base import BaseEntity


@dataclass
class ProductEntity(BaseEntity):
    title: Title
    description: Text
    expiry_date: ExpiresDate
    image_url: Text
    ingredients: Text
    manufacturer: Text

    def __hash__(self) -> int:
        return hash(self.oid)

    def __eq__(self, __value: 'ProductEntity') -> bool:
        return self.oid == __value.oid


