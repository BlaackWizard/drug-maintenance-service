from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

from ...domain.entities.product import ProductEntity


@dataclass
class BaseProductRepo(ABC):
    @abstractmethod
    async def check_product_exists_by_title(self, title: str):
        ...

    @abstractmethod
    async def add_product(self, product: ProductEntity):
        ...


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

