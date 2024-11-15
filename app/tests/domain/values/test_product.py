from datetime import datetime

import pytest

from ....domain.entities.pharmacy import PharmacyEntity
from ....domain.entities.product import ProductEntity
from ....domain.exceptions.product import (EmptyTextException,
                                           ExpiresDateException,
                                           TitleTooLongException, PriceIsNegativeValueException,
                                           )
from ....domain.values.product import ExpiresDate, Text, Title, Price


def test_create_product_success():
    title = Title('Синупрет драже')
    description = Text('Лечит все болезни')
    expiry_date = ExpiresDate(datetime(2025, 1, 7))
    image_url = Text('https://letsenhance.io/static/73136da51c245e80edc6ccfe44888a99/1015f/MainBefore.jpg')
    ingredients = Text("...")
    manufacturer = Text("Китай")

    product = ProductEntity(
        title=title,
        description=description,
        expiry_date=expiry_date,
        image_url=image_url,
        ingredients=ingredients,
        manufacturer=manufacturer,
    )
    assert product.title == title
    assert product.expiry_date == expiry_date


def test_title_is_too_long():
    with pytest.raises(TitleTooLongException):
        Title('a' * 500)


def test_text_is_empty():
    with pytest.raises(EmptyTextException):
        Text('')


def test_price_is_less_than_zero():
    with pytest.raises(PriceIsNegativeValueException):
        Price(-123)


def test_expiration_date_expired():
    with pytest.raises(ExpiresDateException):
        ExpiresDate(datetime(2023, 1, 1))


def test_create_pharmacy():
    title = "Apteka"
    description = "apteka"
    pharmacy = PharmacyEntity(
        title=title,
        description=description,
    )
    assert pharmacy.title == title
    assert pharmacy.description == description


def test_add_product_to_pharmacy():
    title = Title('Синупрет драже')
    description = Text('Лечит все болезни')
    expiry_date = ExpiresDate(datetime(2025, 1, 7))
    image_url = Text('https://letsenhance.io/static/73136da51c245e80edc6ccfe44888a99/1015f/MainBefore.jpg')
    ingredients = Text("...")
    manufacturer = Text("Китай")

    product = ProductEntity(
        title=title,
        description=description,
        expiry_date=expiry_date,
        image_url=image_url,
        ingredients=ingredients,
        manufacturer=manufacturer,
    )

    title_pharmacy = Title("apteka")
    description_pharmacy = Text("apteka")

    pharmacy = PharmacyEntity(
        title=title_pharmacy,
        description=description_pharmacy,
    )
    price = Price(100.020)
    pharmacy.add_product(product=product, price=price)

    assert product in pharmacy.products

