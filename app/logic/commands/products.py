from dataclasses import dataclass
from datetime import datetime

from ...domain.entities.product import ProductEntity
from ...domain.values.product import ExpiresDate, Text, Title
from ...infra.repositories.base import BaseProductRepo
from ...logic.commands.base import BaseCommand, CommandHandler
from ..exceptions.products import ProductWithThatTitleAlreadyExistsException, ProductNotFoundWithThisQuery


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
            ingredients=command.ingredients,
        )
        product_entity = await self.product_repository.get_product_by_oid(command.oid)
        return product_entity


@dataclass(frozen=True)
class DeleteProductCommand(BaseCommand):
    product_oid: str


@dataclass(frozen=True)
class DeleteProductHandler(CommandHandler[DeleteProductCommand, None]):
    product_repository: BaseProductRepo

    async def handle(self, command: DeleteProductCommand) -> None:
        await self.product_repository.delete_product(
            product_oid=command.product_oid,
        )


@dataclass(frozen=True)
class FindProductCommand(BaseCommand):
    product_title: str


@dataclass(frozen=True)
class FindProductHandler(CommandHandler[FindProductCommand, list]):
    product_repository: BaseProductRepo

    async def handle(self, command: FindProductCommand) -> list:
        products = await self.product_repository.search_product(command.product_title)
        if products == []:
            raise ProductNotFoundWithThisQuery

        for product in products:
            del product['_id']

        return products
