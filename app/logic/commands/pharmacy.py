from dataclasses import dataclass

from app.domain.entities.pharmacy import PharmacyEntity
from app.domain.values.product import Price, Text, Title
from app.infra.repositories.base import BasePharmacyRepo, BaseProductRepo
from app.logic.commands.base import BaseCommand, CommandHandler
from app.logic.exceptions.pharmacy import (
    PharmacyByTitleAlreadyExistsException, PharmacyOrProductNotExistsException)


@dataclass(frozen=True)
class CreatePharmacyCommand(BaseCommand):
    title: str
    description: str


@dataclass(frozen=True)
class AddProductCommand(BaseCommand):
    product_oid: str
    pharmacy_oid: str
    price: Price


@dataclass(frozen=True)
class PharmacyHandler(CommandHandler[CreatePharmacyCommand, PharmacyEntity]):
    pharmacy_repository: BasePharmacyRepo

    async def handle(self, command: CreatePharmacyCommand) -> PharmacyEntity:
        if await self.pharmacy_repository.check_pharmacy_exists_by_title(title=command.title):
            raise PharmacyByTitleAlreadyExistsException(title=command.title)

        title = Title(value=command.title)
        description = Text(value=command.description)

        new_pharmacy = PharmacyEntity.create_pharmacy(title=title, description=description)

        await self.pharmacy_repository.add_pharmacy(new_pharmacy)

        return new_pharmacy


@dataclass(frozen=True)
class AddProductHandler(CommandHandler[AddProductCommand, PharmacyEntity]):
    pharmacy_repository: BasePharmacyRepo
    product_repository: BaseProductRepo

    async def handle(self, command: AddProductCommand) -> PharmacyEntity:
        pharmacy = await self.pharmacy_repository.get_pharmacy_by_oid(command.pharmacy_oid)
        product = await self.product_repository.get_product_by_oid(command.product_oid)

        if not pharmacy or product:
            raise PharmacyOrProductNotExistsException

        pharmacy.add_product(product, command.price)

        return pharmacy
