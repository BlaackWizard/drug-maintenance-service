from punq import Container
from pytest import fixture

from ..infra.repositories.pharmacy import BasePharmacyRepo
from ..infra.repositories.products import BaseProductRepo
from ..logic.mediator import Mediator
from .fixtures import init_dummy_container


@fixture(scope='function')
def container() -> Container:
    return init_dummy_container()


@fixture()
def mediator(container: Container) -> Mediator:
    return container.resolve(Mediator)


@fixture()
def pharmacy_repository(container: Container) -> BasePharmacyRepo:
    return container.resolve(BasePharmacyRepo)


@fixture()
def product_repository(container: Container) -> BaseProductRepo:
    return container.resolve(BaseProductRepo)
