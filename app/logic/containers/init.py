from functools import lru_cache

from punq import Container, Scope

from app.logic.commands.pharmacy import AddProductWithPriceCommand  # noqa
from app.logic.commands.pharmacy import AddProductWithPriceHandler  # noqa
from app.logic.commands.pharmacy import ChangeProductPriceCommand  # noqa
from app.logic.commands.pharmacy import ChangeProductPriceHandler  # noqa
from app.logic.commands.pharmacy import DeletePharmacyCommand  # noqa
from app.logic.commands.products import CreateProductCommand  # noqa
from app.logic.commands.products import CreateProductCommandHandler  # noqa
from app.logic.commands.products import DeleteProductCommand  # noqa
from app.logic.commands.products import DeleteProductHandler  # noqa
from app.logic.commands.products import GetProductByOidCommand  # noqa
from app.logic.containers.handlers import init_handler_dependencies
from app.logic.containers.mediators import register_mediator_commands
from app.logic.containers.repositories import init_repository_dependencies
from app.logic.mediator import Mediator
from app.settings.config import Config


def init_base_container() -> Container:
    container = Container()
    container.register(Config, instance=Config(), scope=Scope.singleton)

    def init_mediator():
        mediator = Mediator()
        return mediator

    container.register(Mediator, factory=init_mediator)
    return container


@lru_cache(1)
def init_container():
    return _init_container()


def _init_container() -> Container:
    container = init_base_container()
    mediator = container.resolve(Mediator)
    container.register(Config, instance=Config(), scope=Scope.singleton)

    init_handler_dependencies(container)

    init_repository_dependencies(container)

    register_mediator_commands(container, mediator)

    return container
