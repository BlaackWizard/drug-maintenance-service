from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

from app.domain.entities.pharmacy import PharmacyEntity
from app.domain.entities.product import ProductEntity
from app.domain.values.product import Title, Text, ExpiresDate, Price


@dataclass
class BaseProductRepo(ABC):
    @abstractmethod
    async def check_product_exists_by_title(self, title: str):
        ...

    @abstractmethod
    async def add_product(self, product: ProductEntity):
        ...

    @abstractmethod
    async def get_product_by_oid(self, oid: str) -> ProductEntity:
        ...

    @abstractmethod
    async def update_product(
            self,
            oid: str,
            title: Title,
            description: Text,
            expiry_date: ExpiresDate,
            image_url: Text,
            ingredients: Text,
            manufacturer: Title,
    ):
        ...


@dataclass
class BasePharmacyRepo(ABC):
    @abstractmethod
    async def check_pharmacy_exists_by_title(self, title: str):
        ...

    @abstractmethod
    async def add_pharmacy(self, pharmacy: PharmacyEntity):
        ...

    @abstractmethod
    async def get_pharmacy_by_oid(self, oid: str) -> PharmacyEntity:
        ...

    @abstractmethod
    async def update_pharmacy(self, oid: str, title: Title, description: Text):
        ...

    @abstractmethod
    async def add_product_to_pharmacy(self, pharmacy_oid: str, product_oid: str, price: Price):
        ...

    @abstractmethod
    async def update_product_price_in_pharmacy(
            self,
            pharmacy_oid: str,
            product_oid: str,
            price: Price
    ):
        ...