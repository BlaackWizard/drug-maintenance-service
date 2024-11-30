from dataclasses import dataclass, field
from typing import List

from ..events.pharmacy import NewPharmacyCreatedEvent
from ..events.product import ProductAddedToPharmacyEvent
from ..values.product import Text, Title
from .base import BaseEntity
from .product import ProductEntity


@dataclass
class PharmacyEntity(BaseEntity):
    title: Title
    description: Text
    products: List[dict] = field(default_factory=list, kw_only=True)

    def add_product_with_price(self, product: ProductEntity, price: float):
        """
        Добавление продукта в аптеку с указанием цены.
        """
        self.products.append({product: price})

        self.register_event(
            ProductAddedToPharmacyEvent(
                product_oid=product.oid,
                title=product.title,
                description=product.description,
                expiry_date=product.expiry_date,
                image_url=product.image_url,
                ingredients=product.ingredients,
                manufacturer=product.manufacturer,
                price=price,
                pharmacy_oid=self.oid,
            ),
        )

    @classmethod
    def create_pharmacy(cls, title: Title, description: Text):
        new_pharmacy = cls(title=title, description=description)
        new_pharmacy.register_event(
            NewPharmacyCreatedEvent(
                pharmacy_oid=new_pharmacy.oid,
                title=new_pharmacy.title,
                description=new_pharmacy.description,
            ),
        )
        return new_pharmacy

    def __hash__(self) -> int:
        return hash(self.oid)

    def __eq__(self, __value: 'PharmacyEntity') -> bool:
        return self.oid == __value.oid
