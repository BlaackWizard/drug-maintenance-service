from dataclasses import dataclass

from app.domain.entities.pharmacy import PharmacyEntity
from app.domain.values.product import Price, Text, Title
from app.infra.repositories.base import BasePharmacyRepo, BaseProductRepo
from app.logic.commands.base import BaseCommand, CommandHandler
from app.logic.exceptions.pharmacy import (
    PharmacyByTitleAlreadyExistsException, PharmacyNotFoundException)
from app.logic.exceptions.products import ProductNotFoundException


@dataclass(frozen=True)
class CreatePharmacyCommand(BaseCommand):
    title: Title
    description: Text


@dataclass(frozen=True)
class AddProductWithPriceCommand(BaseCommand):
    pharmacy_oid: str
    product_oid: str
    price: float
    count: int


@dataclass(frozen=True)
class PharmacyHandler(CommandHandler[CreatePharmacyCommand, PharmacyEntity]):
    pharmacy_repository: BasePharmacyRepo

    async def handle(self, command: CreatePharmacyCommand) -> PharmacyEntity:
        if await self.pharmacy_repository.check_pharmacy_exists_by_title(title=command.title.as_generic_type()):
            raise PharmacyByTitleAlreadyExistsException(title=command.title.as_generic_type())

        new_pharmacy = PharmacyEntity.create_pharmacy(
            title=command.title,
            description=command.description,
        )

        await self.pharmacy_repository.add_pharmacy(new_pharmacy)

        return new_pharmacy


@dataclass(frozen=True)
class GetPharmacyByOidCommand(BaseCommand):
    pharmacy_oid: str


@dataclass(frozen=True)
class GetPharmacyByOidHandler(CommandHandler[GetPharmacyByOidCommand, PharmacyEntity]):
    pharmacy_repository: BasePharmacyRepo

    async def handle(self, command: GetPharmacyByOidCommand) -> PharmacyEntity:
        pharmacy = await self.pharmacy_repository.get_pharmacy_by_oid(command.pharmacy_oid)
        return pharmacy


@dataclass(frozen=True)
class UpdatePharmacyCommand(BaseCommand):
    pharmacy_oid: str
    title: Title
    description: Text


@dataclass(frozen=True)
class UpdatePharmacyHandler(CommandHandler[UpdatePharmacyCommand, PharmacyEntity]):
    pharmacy_repository: BasePharmacyRepo

    async def handle(self, command: UpdatePharmacyCommand) -> PharmacyEntity:
        await self.pharmacy_repository.update_pharmacy(
            oid=command.pharmacy_oid,
            title=command.title,
            description=command.description,
        )
        pharmacy_entity = await self.pharmacy_repository.get_pharmacy_by_oid(command.pharmacy_oid)
        return pharmacy_entity


@dataclass(frozen=True)
class ChangeProductPriceCommand(BaseCommand):
    pharmacy_oid: str
    product_oid: str
    price: float


@dataclass(frozen=True)
class ChangeProductPriceHandler(CommandHandler[ChangeProductPriceCommand, PharmacyEntity]):
    pharmacy_repository: BasePharmacyRepo

    async def handle(self, command: ChangeProductPriceCommand) -> PharmacyEntity:
        await self.pharmacy_repository.update_product_price_in_pharmacy(
            pharmacy_oid=command.pharmacy_oid,
            product_oid=command.product_oid,
            price=Price(command.price),
        )
        pharmacy_entity = await self.pharmacy_repository.get_pharmacy_by_oid(command.pharmacy_oid)

        return pharmacy_entity


@dataclass(frozen=True)
class AddProductWithPriceHandler(CommandHandler[AddProductWithPriceCommand, PharmacyEntity]):
    pharmacy_repository: BasePharmacyRepo
    product_repository: BaseProductRepo

    async def handle(self, command: AddProductWithPriceCommand) -> PharmacyEntity:
        pharmacy = await self.pharmacy_repository.get_pharmacy_by_oid(command.pharmacy_oid)
        if not pharmacy:
            raise PharmacyNotFoundException

        product = await self.product_repository.get_product_by_oid(command.product_oid)
        if not product:
            raise ProductNotFoundException

        pharmacy.add_product_with_price(product=product, price=command.price)

        await self.pharmacy_repository.add_product_to_pharmacy(
            pharmacy_oid=pharmacy.oid,
            product_oid=product.oid,
            price=Price(command.price),
            count=command.count,
        )

        return pharmacy


@dataclass(frozen=True)
class DeleteProductFromPharmacyCommand(BaseCommand):
    pharmacy_oid: str
    product_oid: str


@dataclass(frozen=True)
class DeleteProductFromPharmacyHandler(CommandHandler[DeleteProductFromPharmacyCommand, None]):
    pharmacy_repository: BasePharmacyRepo

    async def handle(self, command: DeleteProductFromPharmacyCommand) -> None:
        await self.pharmacy_repository.delete_product_in_pharmacy(
            pharmacy_oid=command.pharmacy_oid,
            product_oid=command.product_oid,
        )


@dataclass(frozen=True)
class DeletePharmacyCommand(BaseCommand):
    pharmacy_oid: str


@dataclass(frozen=True)
class DeletePharmacyHandler(CommandHandler[DeletePharmacyCommand, None]):
    pharmacy_repository: BasePharmacyRepo

    async def handle(self, command: DeletePharmacyCommand) -> None:
        await self.pharmacy_repository.delete_pharmacy(
            pharmacy_oid=command.pharmacy_oid,
        )
