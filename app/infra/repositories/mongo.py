from dataclasses import dataclass

from motor.core import AgnosticClient

from ...domain.entities.pharmacy import PharmacyEntity
from ...domain.entities.product import ProductEntity
from ...infra.repositories.converters import (convert_document_to_pharmacy,
                                              convert_document_to_product,
                                              convert_pharmacy_to_document,
                                              convert_product_to_document)
from .base import BasePharmacyRepo, BaseProductRepo


@dataclass
class MongoDBPharmacyRepo(BasePharmacyRepo):
    mongo_db_client: AgnosticClient
    mongo_db_db_name: str
    mongo_db_collection_name: str

    def _get_pharmacy_collection(self):
        return self.mongo_db_client[self.mongo_db_db_name][self.mongo_db_collection_name]

    async def check_pharmacy_exists_by_title(self, title: str):
        collection = self._get_pharmacy_collection()
        return await collection.find_one(filter={'title': title})

    async def add_pharmacy(self, pharmacy: PharmacyEntity):
        collection = self._get_pharmacy_collection()
        await collection.insert_one(convert_pharmacy_to_document(pharmacy))

    async def get_pharmacy_by_oid(self, oid: str) -> PharmacyEntity:
        collection = self._get_pharmacy_collection()

        pharmacy_document = await collection.find_one({"oid": oid})

        if not pharmacy_document:
            raise ValueError('Pharmacy not found')

        pharmacy_entity = convert_document_to_pharmacy(pharmacy_document)

        return pharmacy_entity


@dataclass
class MongoDBProductRepo(BaseProductRepo):
    mongo_db_client: AgnosticClient
    mongo_db_db_name: str
    mongo_db_collection_name: str

    def _get_product_collection(self):
        return self.mongo_db_client[self.mongo_db_db_name][self.mongo_db_collection_name]

    async def check_product_exists_by_title(self, title: str):
        collection = self._get_product_collection()
        return await collection.find_one(filter={'title': title})

    async def add_product(self, product: ProductEntity):
        collection = self._get_product_collection()
        await collection.insert_one(convert_product_to_document(product))

    async def get_product_by_oid(self, oid: str) -> ProductEntity:
        collection = self._get_product_collection()

        product_document = await collection.find_one({'oid': oid})

        if not product_document:
            raise ValueError('Product not found')

        product_entity = convert_document_to_product(product_document)

        return product_entity
