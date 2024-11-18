from punq import Container, Scope

from ..infra.repositories.pharmacy import BasePharmacyRepo, MemoryPharmacyRepo
from ..logic.init import _init_container


def init_dummy_container() -> Container:
    container = _init_container()
    container.register(BasePharmacyRepo, MemoryPharmacyRepo, scope=Scope.singleton)

    return container