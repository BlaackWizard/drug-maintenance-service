from typing import Dict, List, Optional

from pydantic import BaseModel

from app.domain.entities.pharmacy import PharmacyEntity


class CreatePharmacyRequestSchema(BaseModel):
    title: str
    description: str


class CreatePharmacyResponseSchema(BaseModel):
    oid: str
    title: str
    description: str
    products: Optional[List[str]] = None
    prices: Optional[Dict[str, float]] = None

    @classmethod
    def from_entity(cls, pharmacy: PharmacyEntity) -> 'CreatePharmacyResponseSchema':
        return cls(
            oid=pharmacy.oid,
            title=pharmacy.title.as_generic_type(),
            description=pharmacy.description.as_generic_type(),
            products=pharmacy.products,
            prices=pharmacy.prices,
        )
