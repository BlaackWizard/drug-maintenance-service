from dataclasses import dataclass
from .base import BaseEntity
from ..values.product import Text, Title, ExpiresDate


@dataclass
class ProductEntity(BaseEntity):
    title: Title
    description: Text
    expiry_date: ExpiresDate
    image_url: Text
    ingredients: Text
    manufacturer: Text

