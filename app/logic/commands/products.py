from dataclasses import dataclass
from datetime import datetime

from ...domain.entities.pharmacy import PharmacyEntity
from ...domain.entities.product import ProductEntity
from ...domain.values.product import ExpiresDate, Price, Text, Title
from ...infra.repositories.base import BasePharmacyRepo, BaseProductRepo
from ...logic.commands.base import BaseCommand, CommandHandler
from ..exceptions.pharmacy import PharmacyOrProductNotExistsException
from ..exceptions.products import ProductWithThatTitleAlreadyExistsException


@dataclass(frozen=True)
class CreateProductCommand(BaseCommand):
    title: str
    description: str
    expiry_date: datetime
    image_url: str
    ingredients: str
    manufacturer: str


@dataclass(frozen=True)
class CreateProductCommandHandler(CommandHandler[CreateProductCommand, ProductEntity]):
    product_repository: BaseProductRepo

    async def handle(self, command: CreateProductCommand) -> ProductEntity:

        if await self.product_repository.check_product_exists_by_title(title=command.title):
            raise ProductWithThatTitleAlreadyExistsException(command.title)

        title = Title(command.title)
        description = Text(command.description)
        expiry_date = ExpiresDate(command.expiry_date)
        image_url = Text(command.image_url)
        ingredients = Text(command.ingredients)
        manufacturer = Title(command.manufacturer)

        new_product = ProductEntity.create_product(
            title=title,
            description=description,
            expiry_date=expiry_date,
            image_url=image_url,
            ingredients=ingredients,
            manufacturer=manufacturer,
        )
        await self.product_repository.add_product(new_product)

        return new_product


@dataclass(frozen=True)
class AddProductToPharmacyCommand(BaseCommand):
    product_oid: str
    pharmacy_oid: str
    price: float


@dataclass(frozen=True)
class AddProductToPharmacyHandler(CommandHandler[AddProductToPharmacyCommand, PharmacyEntity]):
    pharmacy_repository: BasePharmacyRepo
    product_repository: BaseProductRepo

    async def handle(self, command: AddProductToPharmacyCommand) -> PharmacyEntity:
        pharmacy = await self.pharmacy_repository.get_pharmacy_by_oid(command.pharmacy_oid)
        product = await self.product_repository.get_product_by_oid(command.product_oid)

        if not product or not pharmacy:
            raise PharmacyOrProductNotExistsException

        price = Price(command.price)

        pharmacy.add_product_with_price(product, price)

        return pharmacy
