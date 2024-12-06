from motor.motor_asyncio import AsyncIOMotorClient
from punq import Scope

from app.infra.repositories.base import BaseProductRepo, BasePharmacyRepo
from app.infra.repositories.mongo import MongoDBPharmacyRepo, MongoDBProductRepo
from app.settings.config import Config


def init_repository_dependencies(container):
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

