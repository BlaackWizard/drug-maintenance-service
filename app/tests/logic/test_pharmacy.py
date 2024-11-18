import pytest
from faker import Faker

from ...domain.entities.pharmacy import PharmacyEntity
from ...domain.values.product import Text, Title
from ...infra.repositories.pharmacy import BasePharmacyRepo
from ...logic.commands.pharmacy import CreatePharmacyCommand
from ...logic.exceptions.pharmacy import PharmacyByTitleAlreadyExistsException
from ...logic.mediator import Mediator


@pytest.mark.asyncio
async def test_create_pharmacy_command_success(
    pharmacy_repository: BasePharmacyRepo,
    mediator: Mediator,
    faker: Faker,
):
    title = Title(faker.text())
    description = Text(faker.text())

    pharmacy: PharmacyEntity
    pharmacy, *_ = await mediator.handle_command(
        CreatePharmacyCommand(
            title=title.as_generic_type(),
            description=description.as_generic_type(),
        ),
    )

    assert await pharmacy_repository.check_pharmacy_exists_by_title(title=pharmacy.title)


@pytest.mark.asyncio
async def test_create_pharmacy_command_title_already_exists(
    pharmacy_repository: BasePharmacyRepo,
    mediator: Mediator,
    faker: Faker,
):
    title = Title(value=faker.text())
    description = Text(value=faker.text())

    pharmacy = PharmacyEntity(title=title.as_generic_type(), description=description.as_generic_type())
    await pharmacy_repository.add_pharmacy(pharmacy)

    assert pharmacy in pharmacy_repository._saved_pharmacies

    with pytest.raises(PharmacyByTitleAlreadyExistsException):
        await mediator.handle_command(
            CreatePharmacyCommand(
                title=title.as_generic_type(),
                description=description.as_generic_type(),
            ),
        )

    assert len(pharmacy_repository._saved_pharmacies) == 1
