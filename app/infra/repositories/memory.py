from dataclasses import dataclass, field
from typing import List

from ...domain.entities.pharmacy import PharmacyEntity
from ...domain.entities.product import ProductEntity
from .base import BasePharmacyRepo, BaseProductRepo


@dataclass
class MemoryPharmacyRepo(BasePharmacyRepo):

    _saved_pharmacies: List[PharmacyEntity] = field(
        default_factory=list,
        kw_only=True,
    )

    async def check_pharmacy_exists_by_title(self, title: str):
        try:
            return bool(
                next(
                    pharmacy for pharmacy in self._saved_pharmacies if pharmacy.title.as_generic_type() == title
                ),
            )
        except StopIteration:
            return False

    async def add_pharmacy(self, pharmacy: PharmacyEntity):
        self._saved_pharmacies.append(pharmacy)

    async def get_pharmacy_by_oid(self, oid: str) -> PharmacyEntity:
        for pharmacy in self._saved_pharmacies:
            if pharmacy.oid == oid:
                return pharmacy


@dataclass
class MemoryProductRepo(BaseProductRepo):
    _saved_products: List[ProductEntity] = field(default_factory=list)

    async def check_product_exists_by_title(self, title: str):
        try:
            return bool(
                next(
                    product for product in self._saved_products if product.title.as_generic_type() == title
                ),
            )
        except StopIteration:
            return False

    async def add_product(self, product: ProductEntity):
        self._saved_products.append(product)

    async def get_product_by_oid(self, oid: str) -> ProductEntity:
        for product in self._saved_products:
            if product.oid == oid:
                return product
