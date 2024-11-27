from dataclasses import dataclass
from datetime import datetime

from .base import CT, CR
from ...domain.entities.pharmacy import PharmacyEntity
from ...domain.entities.product import ProductEntity
from ...domain.values.product import ExpiresDate, Price, Text, Title
from ...infra.repositories.base import BasePharmacyRepo, BaseProductRepo
from ...infra.repositories.converters import convert_document_to_product
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


@dataclass(frozen=True)
class GetProductByOidCommand(BaseCommand):
    product_oid: str


@dataclass(frozen=True)
class GetProductByOidHandler(CommandHandler[GetProductByOidCommand, ProductEntity]):
    product_repository: BaseProductRepo

    async def handle(self, command: GetProductByOidCommand) -> ProductEntity:
        product = await self.product_repository.get_product_by_oid(oid=command.product_oid)
        return product


@dataclass(frozen=True)
class UpdateProductCommand(BaseCommand):
    oid: str
    title: Title
    description: Text
    expiry_date: ExpiresDate
    image_url: Text
    ingredients: Text
    manufacturer: Title


@dataclass(frozen=True)
class UpdateProductHandler(CommandHandler[UpdateProductCommand, ProductEntity]):
    product_repository: BaseProductRepo

    async def handle(self, command: UpdateProductCommand) -> ProductEntity:
        await self.product_repository.update_product(
            oid=command.oid,
            title=command.title,
            description=command.description,
            image_url=command.image_url,
            manufacturer=command.manufacturer,
            expiry_date=command.expiry_date,
            ingredients=command.ingredients
        )
        product_entity = await self.product_repository.get_product_by_oid(command.oid)
        return product_entity

