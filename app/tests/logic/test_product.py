from datetime import datetime

import pytest
from faker import Faker

from ...domain.entities.pharmacy import PharmacyEntity
from ...domain.entities.product import ProductEntity
from ...domain.exceptions.product import ExpiresDateException
from ...domain.values.product import Title, Text, ExpiresDate, Price
from ...infra.repositories.pharmacy import BasePharmacyRepo
from ...infra.repositories.products import BaseProductRepo
from ...logic.commands.pharmacy import CreatePharmacyCommand
from ...logic.commands.products import CreateProductCommand
from ...logic.exceptions.products import ProductWithThatTitleAlreadyExistsException, ProductExpiresDateException
from ...logic.mediator import Mediator


@pytest.mark.asyncio
async def test_create_product_success(
    product_repository: BaseProductRepo,
    mediator: Mediator,
    faker: Faker
):
    title = Title(faker.text())
    description = Text(faker.text())
    expiry_date = ExpiresDate(datetime(2025, 2, 15))
    image_url = Text(faker.text())
    ingredients = Text(faker.text())
    manufacturer = Title(faker.text())

    product: ProductEntity
    product, *_ = await mediator.handle_command(CreateProductCommand(
        title=title.as_generic_type(),
        description=description.as_generic_type(),
        expiry_date=expiry_date.as_generic_type(),
        image_url=image_url.as_generic_type(),
        ingredients=ingredients.as_generic_type(),
        manufacturer=manufacturer.as_generic_type(),
    ))

    assert await product_repository.check_product_exists_by_title(title=title.as_generic_type())


@pytest.mark.asyncio
async def test_create_command_title_already_exists_and_check_expiry_date(
        product_repository: BaseProductRepo,
        mediator: Mediator,
        faker: Faker
):
    title = Title(faker.text())
    description = Text(faker.text())
    expiry_date = ExpiresDate(datetime(2025, 2, 15))
    image_url = Text(faker.text())
    ingredients = Text(faker.text())
    manufacturer = Title(faker.text())

    product = ProductEntity(
        title=title,
        description=description,
        expiry_date=expiry_date,
        image_url=image_url,
        ingredients=image_url,
        manufacturer=manufacturer,
    )
    await product_repository.add_product(product)

    assert product in product_repository._saved_products

    with pytest.raises(ProductWithThatTitleAlreadyExistsException):
        await mediator.handle_command(CreateProductCommand(
            title=title.as_generic_type(),
            description=description.as_generic_type(),
            expiry_date=expiry_date.as_generic_type(),
            image_url=image_url.as_generic_type(),
            ingredients=ingredients.as_generic_type(),
            manufacturer=manufacturer.as_generic_type(),
        ))
    new_title = Title(faker.text())
    with pytest.raises(ExpiresDateException):
        await mediator.handle_command(CreateProductCommand(
            title=new_title.as_generic_type(),
            description=description.as_generic_type(),
            expiry_date=ExpiresDate(datetime(2023, 1, 1)).as_generic_type(),
            image_url=image_url.as_generic_type(),
            ingredients=ingredients.as_generic_type(),
            manufacturer=manufacturer.as_generic_type(),
        ))
    assert len(product_repository._saved_products) == 1


@pytest.mark.asyncio
async def test_create_product_to_pharmacy(
        product_repository: BaseProductRepo,
        pharmacy_repository: BasePharmacyRepo,
        mediator: Mediator,
        faker: Faker
):
    pharmacy_title = Title(faker.text())
    pharmacy_description = Text(faker.text())

    pharmacy: PharmacyEntity
    pharmacy, *_ = await mediator.handle_command(
        CreatePharmacyCommand(
            title=pharmacy_title,
            description=pharmacy_description,
        ),
    )

    assert await pharmacy_repository.check_pharmacy_exists_by_title(title=pharmacy.title.as_generic_type())

    title = Title(faker.text())
    description = Text(faker.text())
    expiry_date = ExpiresDate(datetime(2025, 2, 15))
    image_url = Text(faker.text())
    ingredients = Text(faker.text())
    manufacturer = Title(faker.text())

    product: ProductEntity
    product, *_ = await mediator.handle_command(CreateProductCommand(
        title=title.as_generic_type(),
        description=description.as_generic_type(),
        expiry_date=expiry_date.as_generic_type(),
        image_url=image_url.as_generic_type(),
        ingredients=ingredients.as_generic_type(),
        manufacturer=manufacturer.as_generic_type(),
    ))

    assert await product_repository.check_product_exists_by_title(title=title.as_generic_type())

    price = Price(100.123)
    pharmacy.add_product(product, price)
    product_price = pharmacy.prices.get(product)


    assert product in pharmacy.products
    assert product_price.price.as_generic_type() == price.as_generic_type()



