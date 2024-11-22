from abc import ABC, abstractmethod
from dataclasses import dataclass

from app.domain.entities.pharmacy import PharmacyEntity
from app.domain.entities.product import ProductEntity


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
