from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    mongodb_connection_uri: str = Field(alias='MONGO_DB_CONNECTION_URI')
    mongodb_pharmacy_database: str = Field(default='drug-service', alias='MONGODB_PHARMACY_DATABASE')
    mongodb_pharmacy_collection: str = Field(default='pharmacy_collection', alias='MONGODB_PHARMACY_COLLECTION')
    mongodb_product_collection: str = Field(
        default='products_collection',
        alias='MONGODB_PRODUCT_COLLECTION',
    )
