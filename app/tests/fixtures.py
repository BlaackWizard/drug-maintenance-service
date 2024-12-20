from punq import Container, Scope

from app.logic.containers.init import _init_container

from ..infra.repositories.base import BasePharmacyRepo, BaseProductRepo
from ..infra.repositories.mongo import MongoDBPharmacyRepo, MongoDBProductRepo


def init_dummy_container() -> Container:
    container = _init_container()
    container.register(BasePharmacyRepo, MongoDBPharmacyRepo, scope=Scope.singleton)
    container.register(BaseProductRepo, MongoDBProductRepo, scope=Scope.singleton)

    return container
