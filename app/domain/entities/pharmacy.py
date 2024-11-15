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
                product_id=product.id,
                title=product.title,
                description=product.description,
                expiry_date=product.expiry_date,
                image_url=product.image_url,
                ingredients=product.ingredients,
                manufacturer=product.manufacturer,
                pharmacy_id=self.id,
            ),
        )
