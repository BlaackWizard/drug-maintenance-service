from functools import lru_cache

from punq import Container, Scope

from ..infra.repositories.pharmacy import BasePharmacyRepo, MemoryPharmacyRepo
from ..infra.repositories.products import BaseProductRepo, MemoryProductRepo
from .commands.pharmacy import CreatePharmacyCommand, PharmacyHandler  # noqa
from .commands.products import CreateProductCommand  # noqa
from .commands.products import CreateProductCommandHandler  # noqa
from .mediator import Mediator


@lru_cache(1)
def init_container():
    return _init_container()


def _init_container() -> Container:
    container = Container()
    container.register(BasePharmacyRepo, MemoryPharmacyRepo, scope=Scope.singleton)
    container.register(BaseProductRepo, MemoryProductRepo, scope=Scope.singleton)
    container.register(CreateProductCommandHandler)
    container.register(PharmacyHandler)

    def init_mediator():
        mediator = Mediator()
        mediator.register_command(
            CreatePharmacyCommand,
            [container.resolve(PharmacyHandler)],
        )
        mediator.register_command(
            CreateProductCommand,
            [container.resolve(CreateProductCommandHandler)],
        )
        return mediator

    container.register(Mediator, factory=init_mediator)

    return container
