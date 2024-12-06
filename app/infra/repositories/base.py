from abc import ABC, abstractmethod
from dataclasses import dataclass

from app.domain.entities.pharmacy import PharmacyEntity
from app.domain.entities.product import ProductEntity
from app.domain.values.product import ExpiresDate, Price, Text, Title


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

    @abstractmethod
    async def delete_product(
            self,
            product_oid: str,
    ):
        ...

    @abstractmethod
    async def search_product(self, query: str):
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
    async def add_product_to_pharmacy(self, pharmacy_oid: str, product_oid: str, price: Price, count: int):
        ...

    @abstractmethod
    async def update_product_price_in_pharmacy(
            self,
            pharmacy_oid: str,
            product_oid: str,
            price: Price,
    ):
        ...

    @abstractmethod
    async def delete_product_in_pharmacy(
            self,
            pharmacy_oid: str,
            product_oid: str,
    ):
        ...

    @abstractmethod
    async def delete_pharmacy(
            self,
            pharmacy_oid: str,
    ):
        ...

    @abstractmethod
    async def find_pharmacy(
        self,
        pharmacy_title: str
    ):
        ...
