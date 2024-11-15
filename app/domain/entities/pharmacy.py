from dataclasses import dataclass, field

from ..events.product import NewProductReceivedEvent
from ..values.product import Text, Title
from .base import BaseEntity
from .product import ProductEntity


@dataclass
class PharmacyEntity(BaseEntity):
    title: Title
    description: Text
    products: set[ProductEntity] = field(default_factory=set, kw_only=True)

    def add_product(self, product: ProductEntity):
        self.products.add(product)
        self.register_event(
            NewProductReceivedEvent(
                product_oid=product.oid,
                title=product.title.as_generic_type(),
                description=product.description.as_generic_type(),
                expiry_date=product.expiry_date.as_generic_type(),
                image_url=product.image_url.as_generic_type(),
                ingredients=product.ingredients.as_generic_type(),
                manufacturer=product.manufacturer.as_generic_type(),
                pharmacy_oid=self.oid,
            ),
        )

    def __hash__(self) -> int:
        return hash(self.oid)

    def __eq__(self, __value: 'PharmacyEntity') -> bool:
        return self.oid == __value.oid
