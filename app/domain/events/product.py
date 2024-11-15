from dataclasses import dataclass

from ..values.product import ExpiresDate, Text, Title, Price
from .base import BaseEvent


@dataclass
class NewProductReceivedEvent(BaseEvent):
    product_oid: str
    title: Title
    description: Text
    expiry_date: ExpiresDate
    image_url: Text
    ingredients: Text
    manufacturer: Text
    price: Price
    pharmacy_oid: str
