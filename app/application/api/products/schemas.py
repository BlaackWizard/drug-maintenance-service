from datetime import datetime

from pydantic import BaseModel

from ....domain.entities.pharmacy import PharmacyEntity
from ....domain.entities.product import ProductEntity


class CreateProductRequestSchema(BaseModel):
    title: str
    description: str
    expiry_date: datetime
    image_url: str
    ingredients: str
    manufacturer: str


class CreateProductResponseSchema(BaseModel):
    product_oid: str
    title: str
    description: str
    expiry_date: datetime
    image_url: str
    ingredients: str
    manufacturer: str

    @classmethod
    def from_entity(cls, product: ProductEntity) -> 'CreateProductResponseSchema':
        return CreateProductResponseSchema(
            product_oid=product.oid,
            title=product.title.as_generic_type(),
            description=product.description.as_generic_type(),
            expiry_date=product.expiry_date.as_generic_type(),
            image_url=product.image_url.as_generic_type(),
            ingredients=product.ingredients.as_generic_type(),
            manufacturer=product.manufacturer.as_generic_type(),
        )


class AddProductToPharmacyResponseSchema(BaseModel):
    oid: str
    title: str
    description: str
    products: list

    @classmethod
    def from_entity(cls, pharmacy: PharmacyEntity) -> 'AddProductToPharmacyResponseSchema':
        return cls(
            oid=pharmacy.oid,
            title=pharmacy.title,
            description=pharmacy.description,
            products=pharmacy.products,
        )


class UpdateProductRequestSchema(BaseModel):
    title: str
    description: str
    expiry_date: datetime
    image_url: str
    ingredients: str
    manufacturer: str


class AddProductToPharmacyRequestSchema(BaseModel):
    product_oid: str
    pharmacy_oid: str
    price: float
    count: int


class DeleteProductRequestSchema(BaseModel):
    product_oid: str


class FindProductRequestSchema(BaseModel):
    product_title: str


class FindProductResponseSchema(BaseModel):
    products: list

