from functools import lru_cache

from punq import Container, Scope

from ..infra.repositories.pharmacy import BasePharmacyRepo, MemoryPharmacyRepo
from .commands.pharmacy import CreatePharmacyCommand, PharmacyHandler  # noqa
from .mediator import Mediator


@lru_cache(1)
def init_container():
    return _init_container()


def _init_container() -> Container:
    container = Container()
    container.register(BasePharmacyRepo, MemoryPharmacyRepo, scope=Scope.singleton)
    container.register(PharmacyHandler)

    def init_mediator():
        mediator = Mediator()
        mediator.register_command(
            CreatePharmacyCommand,
            [container.resolve(PharmacyHandler)],
        )
        return mediator

    container.register(Mediator, factory=init_mediator)

    return container
