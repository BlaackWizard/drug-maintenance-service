from dataclasses import dataclass

from app.domain.entities.pharmacy import PharmacyEntity
from app.domain.values.product import Text, Title
from app.infra.repositories.pharmacy import BasePharmacyRepo
from app.logic.commands.base import BaseCommand, CommandHandler
from app.logic.exceptions.pharmacy import PharmacyByTitleAlreadyExistsException


@dataclass(frozen=True)
class CreatePharmacyCommand(BaseCommand):
    title: str
    description: str


@dataclass(frozen=True)
class PharmacyHandler(CommandHandler[CreatePharmacyCommand, PharmacyEntity]):
    pharmacy_repo: BasePharmacyRepo

    async def handle(self, command: CreatePharmacyCommand) -> PharmacyEntity:
        if await self.pharmacy_repo.check_pharmacy_exists_by_title(command.title):
            raise PharmacyByTitleAlreadyExistsException(title=command.title)

        title = Title(value=command.title)
        description = Text(value=command.description)

        new_pharmacy = PharmacyEntity.create_pharmacy(title=title, description=description)

        await self.pharmacy_repo.add_pharmacy(new_pharmacy)

        return new_pharmacy
