from dataclasses import dataclass
from datetime import datetime

from motor.core import AgnosticClient

from ...domain.entities.pharmacy import PharmacyEntity
from ...domain.entities.product import ProductEntity
from ...domain.values.product import Title, Text, ExpiresDate, Price
from ...infra.repositories.converters import (convert_document_to_pharmacy,
                                              convert_document_to_product,
                                              convert_pharmacy_to_document,
                                              convert_product_to_document,
                                              convert_pharmacy_to_document_without_generic_type)
from .base import BasePharmacyRepo, BaseProductRepo
from ...logic.exceptions.pharmacy import PharmacyNotFoundException
from ...logic.exceptions.products import ProductNotFoundException


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
            raise PharmacyNotFoundException

        pharmacy_entity = convert_document_to_pharmacy(pharmacy_document)

        return pharmacy_entity

    async def update_pharmacy(self, oid: str, title: Title, description: Text):
        collection = self._get_pharmacy_collection()

        pharmacy_document = await collection.find_one({"oid": oid})

        if not pharmacy_document:
            raise PharmacyNotFoundException

        await collection.update_one(
                {"oid": oid},
                {"$set": {"title": title.as_generic_type(),
                          "description": description.as_generic_type()}}
            )

    async def add_product_to_pharmacy(self, pharmacy_oid: str, product_oid: str, price: Price):
        collection = self._get_pharmacy_collection()

        pharmacy_document = await collection.find_one({"oid": pharmacy_oid})

        if not pharmacy_document:
            raise PharmacyNotFoundException

        prices = pharmacy_document.get('prices', [])
        if not isinstance(prices, list):
            raise ValueError("Field 'prices' is not an array in the pharmacy document.")

        if any(p['product_oid'] == product_oid for p in prices):
            raise ProductNotFoundException

        await collection.update_one(
            {"oid": pharmacy_oid},
            {"$push": {"prices": {"product_oid": product_oid, "price": price.as_generic_type()}}}
        )

    async def update_product_price_in_pharmacy(
            self,
            pharmacy_oid: str,
            product_oid: str,
            price: Price
    ):
        collection = self._get_pharmacy_collection()
        pharmacy_document = await collection.find_one({"oid": pharmacy_oid})

        if not pharmacy_document:
            raise PharmacyNotFoundException

        if product_oid not in pharmacy_document['prices']:
            raise ProductNotFoundException

        await collection.update_one(
            {"oid": pharmacy_oid, "prices.product_oid": product_oid},
            {"$set": {"prices.$.price": price.as_generic_type()}}
        )


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
            raise ProductNotFoundException

        product_entity = convert_document_to_product(product_document)

        return product_entity

    async def update_product(
            self,
            oid: str,
            title: Title,
            description: Text,
            expiry_date: ExpiresDate,
            image_url: Text,
            ingredients: Text,
            manufacturer: Title,
    ):
        collection = self._get_product_collection()

        product_document = await collection.find_one({"oid": oid})
        if not product_document:
            raise ProductNotFoundException

        await collection.update_one(
            {"oid": oid},
            {"$set": {
                "title": title.as_generic_type(),
                "description": description.as_generic_type(),
                "expiry_date": expiry_date.as_generic_type(),
                "image_url": image_url.as_generic_type(),
                "ingredients": ingredients.as_generic_type(),
                "manufacturer": manufacturer.as_generic_type(),
            }}
        )

