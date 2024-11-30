from ...domain.entities.pharmacy import PharmacyEntity
from ...domain.entities.product import ProductEntity


def convert_product_to_document(product: ProductEntity) -> dict:
    return {
        'oid': product.oid,
        'title': product.title.as_generic_type(),
        'description': product.description.as_generic_type(),
        'manufacturer': product.manufacturer.as_generic_type(),
        'ingredients': product.ingredients.as_generic_type(),
        'expiry_date': product.expiry_date.as_generic_type(),
        'image_url': product.image_url.as_generic_type(),
        'created_at': product.created_at,
    }


def convert_pharmacy_to_document(pharmacy: PharmacyEntity) -> dict:
    return {
        'oid': pharmacy.oid,
        'title': pharmacy.title.as_generic_type(),
        'description': pharmacy.description.as_generic_type(),
        'products': pharmacy.products,
        'created_at': pharmacy.created_at,
    }


def convert_pharmacy_to_document_without_generic_type(pharmacy: PharmacyEntity) -> dict:
    return {
        'oid': pharmacy.oid,
        'title': pharmacy.title,
        'description': pharmacy.description,
        'products': pharmacy.products,
        'created_at': pharmacy.created_at,
    }


def convert_document_to_pharmacy(document: dict) -> PharmacyEntity:
    return PharmacyEntity(
        oid=document['oid'],
        title=document['title'],
        description=document['description'],
        products=document['products'],
        created_at=document['created_at'],
    )


def convert_document_to_product(document: dict) -> ProductEntity:
    return ProductEntity(
        oid=document['oid'],
        title=document['title'],
        description=document['description'],
        manufacturer=document['manufacturer'],
        image_url=document['image_url'],
        ingredients=document['ingredients'],
        expiry_date=document['expiry_date'],
        created_at=document['created_at'],
    )
