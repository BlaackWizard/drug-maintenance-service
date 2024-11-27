from functools import lru_cache

from motor.motor_asyncio import AsyncIOMotorClient
from punq import Container, Scope

from ..infra.repositories.base import BasePharmacyRepo, BaseProductRepo
from ..infra.repositories.mongo import MongoDBPharmacyRepo, MongoDBProductRepo
from ..settings.config import Config
from .commands.pharmacy import CreatePharmacyCommand, PharmacyHandler, GetPharmacyByOidCommand, \
    GetPharmacyByOidHandler, UpdatePharmacyHandler, UpdatePharmacyCommand, ChangeProductPriceHandler, \
    ChangeProductPriceCommand, AddProductWithPriceHandler, AddProductWithPriceCommand  # noqa
from .commands.products import AddProductToPharmacyCommand, GetProductByOidHandler, GetProductByOidCommand, \
    UpdateProductHandler, UpdateProductCommand  # noqa
from .commands.products import CreateProductCommandHandler  # noqa
from .commands.products import (AddProductToPharmacyHandler,  # noqa
                                CreateProductCommand)
from .mediator import Mediator


@lru_cache(1)
def init_container():
    return _init_container()


def _init_container() -> Container:
    container = Container()
    container.register(Config, instance=Config(), scope=Scope.singleton)
    container.register(CreateProductCommandHandler)
    container.register(PharmacyHandler)
    container.register(AddProductToPharmacyHandler)
    container.register(GetProductByOidHandler)
    container.register(GetPharmacyByOidHandler)
    container.register(UpdatePharmacyHandler)
    container.register(UpdateProductHandler)
    container.register(ChangeProductPriceHandler)
    container.register(AddProductWithPriceHandler)

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
        mediator.register_command(
            AddProductToPharmacyCommand,
            [container.resolve(AddProductToPharmacyHandler)],
        )
        mediator.register_command(
            GetProductByOidCommand,
            [container.resolve(GetProductByOidHandler)]
        )
        mediator.register_command(
            GetPharmacyByOidCommand,
            [container.resolve(GetPharmacyByOidHandler)]
        ),
        mediator.register_command(
            UpdatePharmacyCommand,
            [container.resolve(UpdatePharmacyHandler)]
        )
        mediator.register_command(
            UpdateProductCommand,
            [container.resolve(UpdateProductHandler)]
        )
        mediator.register_command(
            ChangeProductPriceCommand,
            [container.resolve(ChangeProductPriceHandler)]
        ),
        mediator.register_command(
            AddProductWithPriceCommand,
            [container.resolve(AddProductWithPriceHandler)]
        )
        return mediator

    def init_pharmacy_mongodb_repository():
        config: Config = container.resolve(Config)
        client = AsyncIOMotorClient(config.mongodb_connection_uri, serverSelectionTimeoutMS=3000)
        return MongoDBPharmacyRepo(
            mongo_db_client=client,
            mongo_db_db_name=config.mongodb_pharmacy_database,
            mongo_db_collection_name=config.mongodb_pharmacy_collection,
        )

    def init_product_mongodb_repository():
        config: Config = container.resolve(Config)
        client = AsyncIOMotorClient(config.mongodb_connection_uri, serverSelectionTimeoutMS=3000)
        return MongoDBProductRepo(
            mongo_db_client=client,
            mongo_db_db_name=config.mongodb_pharmacy_database,
            mongo_db_collection_name=config.mongodb_product_collection,
        )

    container.register(BasePharmacyRepo, factory=init_pharmacy_mongodb_repository, scope=Scope.singleton)
    container.register(BaseProductRepo, factory=init_product_mongodb_repository, scope=Scope.singleton)
    container.register(Mediator, factory=init_mediator)

    return container
