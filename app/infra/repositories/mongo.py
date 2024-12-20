from dataclasses import dataclass

from motor.core import AgnosticClient

from ...domain.entities.pharmacy import PharmacyEntity
from ...domain.entities.product import ProductEntity
from ...domain.values.product import ExpiresDate, Price, Text, Title
from ...infra.repositories.converters import (convert_document_to_pharmacy,
                                              convert_document_to_product,
                                              convert_pharmacy_to_document,
                                              convert_product_to_document)
from ...logic.exceptions.pharmacy import PharmacyNotFoundException
from ...logic.exceptions.products import ProductNotFoundException
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
                {
                    "$set": {
                        "title": title.as_generic_type(),
                        "description": description.as_generic_type(),
                    },
                },
        )

    async def add_product_to_pharmacy(self, pharmacy_oid: str, product_oid: str, price: Price, count: int):
        collection = self._get_pharmacy_collection()

        pharmacy_document = await collection.find_one({"oid": pharmacy_oid})

        if not pharmacy_document:
            raise PharmacyNotFoundException

        products = pharmacy_document.get('products', [])
        if not isinstance(products, list):
            raise ValueError("Field 'prices' is not an array in the pharmacy document.")

        if any(p['product_oid'] == product_oid for p in products):
            raise ProductNotFoundException

        await collection.update_one(
            {"oid": pharmacy_oid},
            {"$push": {"products": {"product_oid": product_oid, "price": price.as_generic_type(), "count": count}}},
        )

    async def update_product_price_in_pharmacy(
            self,
            pharmacy_oid: str,
            product_oid: str,
            price: Price,
    ):
        collection = self._get_pharmacy_collection()
        pharmacy_document = await collection.find_one({"oid": pharmacy_oid})

        if not pharmacy_document:
            raise PharmacyNotFoundException

        product_exists = any(item['product_oid'] == product_oid for item in pharmacy_document['prices'])
        if not product_exists:
            raise ProductNotFoundException

        await collection.update_one(
            {"oid": pharmacy_oid, "prices.product_oid": product_oid},
            {"$set": {"products.$.price": price.as_generic_type()}},
        )

    async def delete_product_in_pharmacy(
            self,
            pharmacy_oid: str,
            product_oid: str,
    ):
        collection = self._get_pharmacy_collection()
        pharmacy_document = await collection.find_one({"oid": pharmacy_oid})

        if not pharmacy_document:
            raise PharmacyNotFoundException

        products_exists = any(item['product_oid'] == product_oid for item in pharmacy_document['products'])

        if not products_exists:
            raise ProductNotFoundException

        await collection.update_one(
            {"oid": pharmacy_oid},
            {"$pull": {"products": {"product_oid": product_oid}}},
        )

    async def delete_pharmacy(
            self,
            pharmacy_oid: str,
    ):
        collection = self._get_pharmacy_collection()

        pharmacy_exists = collection.find_one({"oid": pharmacy_oid})

        if not pharmacy_exists:
            raise PharmacyNotFoundException

        await collection.delete_one(
            {"oid": pharmacy_oid},
        )

    async def find_pharmacy(
        self,
        pharmacy_title: str,
    ):
        collection = self._get_pharmacy_collection()

        result = collection.aggregate([
            {
                "$search": {
                    "index": "language_search",
                    "text": {
                        "query": f'{pharmacy_title}',
                        "path": "title",
                        "fuzzy": {},
                    },
                },
            },
        ])
        pharmacies = await result.to_list(length=300)
        return pharmacies


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

    async def search_product(self, query: str):
        collection = self._get_product_collection()
        result = collection.aggregate([
            {
                "$search": {
                    "index": "product_search",
                    "text": {
                        "query": f'{query}',
                        "path": "title",
                        "fuzzy": {},
                    },
                },
            },
        ])

        results = await result.to_list(length=300)

        return results

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
            {
                "$set": {
                    "title": title.as_generic_type(),
                    "description": description.as_generic_type(),
                    "expiry_date": expiry_date.as_generic_type(),
                    "image_url": image_url.as_generic_type(),
                    "ingredients": ingredients.as_generic_type(),
                    "manufacturer": manufacturer.as_generic_type(),
                },
            },
        )

    async def delete_product(
            self,
            product_oid: str,
    ):
        collection = self._get_product_collection()

        product_document = await collection.find_one({"oid": product_oid})

        if not product_document:
            raise ProductNotFoundException

        await collection.delete_one(
            {"oid": product_oid},
        )
