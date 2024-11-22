from pydantic import BaseModel

from app.domain.entities.pharmacy import PharmacyEntity


class CreatePharmacyRequestSchema(BaseModel):
    title: str
    description: str


class CreatePharmacyResponseSchema(BaseModel):
    oid: str
    title: str
    description: str
    products: set
    prices: dict

    @classmethod
    def from_entity(cls, pharmacy: PharmacyEntity) -> 'CreatePharmacyResponseSchema':
        return CreatePharmacyResponseSchema(
            oid=pharmacy.oid,
            title=pharmacy.title.as_generic_type(),
            description=pharmacy.description.as_generic_type(),
            products=pharmacy.products,
            prices=pharmacy.prices,
        )
