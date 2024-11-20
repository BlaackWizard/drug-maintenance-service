from dataclasses import dataclass

from ..events.product import NewProductReceivedEvent
from ..values.product import ExpiresDate, Text, Title
from .base import BaseEntity


@dataclass
class ProductEntity(BaseEntity):
    title: Title
    description: Text
    expiry_date: ExpiresDate
    image_url: Text
    ingredients: Text
    manufacturer: Title

    @classmethod
    def create_product(
        cls,
        title: Title,
        description: Text,
        expiry_date: ExpiresDate,
        image_url: Text,
        ingredients: Text,
        manufacturer: Title,
    ):
        new_product = cls(
            title=title,
            description=description,
            expiry_date=expiry_date,
            image_url=image_url,
            ingredients=ingredients,
            manufacturer=manufacturer,
        )
        new_product.register_event(
            NewProductReceivedEvent(
                product_oid=new_product.oid,
                title=new_product.title.as_generic_type(),
                description=new_product.description.as_generic_type(),
                expiry_date=new_product.expiry_date.as_generic_type(),
                image_url=new_product.image_url.as_generic_type(),
                ingredients=new_product.ingredients.as_generic_type(),
                manufacturer=new_product.manufacturer.as_generic_type(),
            ),
        )
        return new_product

    def __hash__(self) -> int:
        return hash(self.oid)

    def __eq__(self, __value: 'ProductEntity') -> bool:
        return self.oid == __value.oid
