from datetime import datetime

import pytest

from ....domain.entities.product import ProductEntity
from ....domain.exceptions.product import TitleTooLongException, EmptyTextException, ExpiresDateException
from ....domain.values.product import Text, Title, ExpiresDate


def test_create_product_success():
    product_id = 1
    title = Title('Синупрет драже')
    description = Text('Лечит все болезни')
    expiry_date = ExpiresDate(datetime(2025, 1, 7))
    image_url = Text('https://letsenhance.io/static/73136da51c245e80edc6ccfe44888a99/1015f/MainBefore.jpg')
    ingredients = Text("...")
    manufacturer = Text("Китай")

    product = ProductEntity(
        id=product_id,
        title=title,
        description=description,
        expiry_date=expiry_date,
        image_url=image_url,
        ingredients=ingredients,
        manufacturer=manufacturer
    )
    assert product.title == title
    assert product.expiry_date == expiry_date

def test_title_is_too_long():
    with pytest.raises(TitleTooLongException):
        Title('a' * 500)

def test_text_is_empty():
    with pytest.raises(EmptyTextException):
        Text('')

def test_expiration_date_expired():
    with pytest.raises(ExpiresDateException):
        ExpiresDate(datetime(2023, 1, 1))
