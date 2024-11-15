from dataclasses import dataclass

from ..values.product import ExpiresDate, Text, Title
from .base import BaseEvent


@dataclass
class NewProductReceivedEvent(BaseEvent):
    product_id: int
    title: Title
    description: Text
    expiry_date: ExpiresDate
    image_url: Text
    ingredients: Text
    manufacturer: Text
    pharmacy_id: int
