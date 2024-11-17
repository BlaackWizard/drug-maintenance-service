from pytest import fixture

from ..infra.repositories.pharmacy import BasePharmacyRepo, MemoryPharmacyRepo
from ..logic.init import init_mediator
from ..logic.mediator import Mediator


@fixture(scope='function')
def pharmacy_repository() -> MemoryPharmacyRepo:
    return MemoryPharmacyRepo()


@fixture(scope='function')
def mediator(pharmacy_repository: BasePharmacyRepo) -> Mediator:
    mediator = Mediator()
    init_mediator(mediator=mediator, pharmacy_repo=pharmacy_repository)

    return mediator