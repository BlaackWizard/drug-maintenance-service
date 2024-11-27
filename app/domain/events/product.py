from dataclasses import dataclass

from ..values.product import ExpiresDate, Price, Text, Title
from .base import BaseEvent


@dataclass
class NewProductReceivedEvent(BaseEvent):
    product_oid: str
    title: Title
    description: Text
    expiry_date: ExpiresDate
    image_url: Text
    ingredients: Text
    manufacturer: Title


@dataclass
class ProductAddedToPharmacyEvent(BaseEvent):
    product_oid: str
    title: Title
    description: Text
    expiry_date: ExpiresDate
    image_url: Text
    ingredients: Text
    manufacturer: Title
    price: float
    pharmacy_oid: str
