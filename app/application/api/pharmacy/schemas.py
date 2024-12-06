from typing import Any, Dict, List

from pydantic import BaseModel

from app.domain.entities.pharmacy import PharmacyEntity


class CreatePharmacyRequestSchema(BaseModel):
    title: str
    description: str


class CreatePharmacyResponseSchema(BaseModel):
    oid: str
    title: str
    description: str
    products: List[Dict[str, Any]] = None

    @classmethod
    def from_entity(cls, pharmacy: PharmacyEntity) -> 'CreatePharmacyResponseSchema':
        return cls(
            oid=pharmacy.oid,
            title=pharmacy.title.as_generic_type(),
            description=pharmacy.description.as_generic_type(),
            products=pharmacy.products,
        )


class UpdatePharmacyRequestSchema(BaseModel):
    title: str
    description: str


class ChangeProductPriceRequestSchema(BaseModel):
    pharmacy_oid: str
    product_oid: str
    price: float


class DeleteProductFromPharmacyRequestSchema(BaseModel):
    pharmacy_oid: str
    product_oid: str


class DeletePharmacyRequestSchema(BaseModel):
    pharmacy_oid: str


class FindPharmacyRequestSchema(BaseModel):
    pharmacy_title: str


class FindPharmacyResponseSchema(BaseModel):
    pharmacies: list
