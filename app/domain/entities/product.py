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
