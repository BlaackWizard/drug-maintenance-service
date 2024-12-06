from fastapi import APIRouter, Depends, HTTPException, status

from app.domain.exceptions.base import ApplicationException
from app.logic.containers.init import init_container

from ....domain.values.product import ExpiresDate, Text, Title
from ....logic.commands.pharmacy import AddProductWithPriceCommand
from ....logic.commands.products import (CreateProductCommand,
                                         DeleteProductCommand,
                                         FindProductCommand,
                                         GetProductByOidCommand,
                                         UpdateProductCommand)
from ....logic.mediator import Mediator
from ..schemas import ErrorSchema
from .schemas import (AddProductToPharmacyRequestSchema,
                      AddProductToPharmacyResponseSchema,
                      CreateProductRequestSchema, CreateProductResponseSchema,
                      DeleteProductRequestSchema, FindProductRequestSchema,
                      FindProductResponseSchema, UpdateProductRequestSchema)

router = APIRouter(tags=['Products'])


@router.post(
    '/create-product',
    status_code=status.HTTP_201_CREATED,
    description="Эндпоинт создает новый товар, если товар с таким названием уже существует "
                "или товар уже просрочен, возвращается 400 ошибка",
    responses={
        status.HTTP_201_CREATED: {'model': CreateProductResponseSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema},
    },
)
async def create_product_handler(schema: CreateProductRequestSchema, container=Depends(init_container)):
    '''Создает новый товар'''
    mediator: Mediator = container.resolve(Mediator)

    try:
        product, *_ = await mediator.handle_command(
            CreateProductCommand(
                title=schema.title,
                description=schema.description,
                expiry_date=schema.expiry_date,
                image_url=schema.image_url,
                ingredients=schema.ingredients,
                manufacturer=schema.manufacturer,
            ),
        )
    except ApplicationException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exc.message})

    return CreateProductResponseSchema.from_entity(product)


@router.post(
    '/add-product',
    status_code=status.HTTP_201_CREATED,
    description="Эндпоинт который добавляет товар в аптеку, если product oid или pharmacy oid"
                "не верны, то возвращается 400 ошибка",
    responses={
        status.HTTP_201_CREATED: {'model': AddProductToPharmacyResponseSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema},
    },
)
async def add_product_to_pharmacy_handler(
    schema: AddProductToPharmacyRequestSchema,
    container=Depends(init_container),
) -> AddProductToPharmacyResponseSchema:
    '''Добавляет товар в аптеку с указанием цены'''
    mediator: Mediator = container.resolve(Mediator)

    try:
        pharmacy, *_ = await mediator.handle_command(
            AddProductWithPriceCommand(
                product_oid=schema.product_oid,
                pharmacy_oid=schema.pharmacy_oid,
                price=schema.price,
                count=schema.count,
            ),
        )
    except ApplicationException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exc.message})

    return AddProductToPharmacyResponseSchema.from_entity(pharmacy)


@router.get(
    '/get-product',
    status_code=status.HTTP_200_OK,
    description="Эндпоинт который ищет товар по oid, если его нет возвращается 400 ошибка",
)
async def get_product_by_oid(
    product_oid: str,
    container=Depends(init_container),
) -> CreateProductResponseSchema:
    '''Ищет товар по oid'''
    mediator: Mediator = container.resolve(Mediator)

    try:
        product, *_ = await mediator.handle_command(
            GetProductByOidCommand(
                product_oid=product_oid,
            ),
        )
    except ApplicationException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exc.message})

    return CreateProductResponseSchema(
        product_oid=product.oid,
        title=product.title,
        description=product.description,
        expiry_date=product.expiry_date,
        image_url=product.image_url,
        manufacturer=product.manufacturer,
        ingredients=product.ingredients,
        count=product.count,
    )


@router.post(
    '/update-product',
    status_code=status.HTTP_202_ACCEPTED,
    description="Эндпоинт обновляет данные об товаре",
)
async def update_product(
    product_oid: str,
    schema: UpdateProductRequestSchema,
    container=Depends(init_container),
):
    mediator: Mediator = container.resolve(Mediator)

    try:
        product, *_ = await mediator.handle_command(
            UpdateProductCommand(
                oid=product_oid,
                title=Title(schema.title),
                description=Text(schema.description),
                expiry_date=ExpiresDate(schema.expiry_date),
                image_url=Text(schema.image_url),
                ingredients=Text(schema.ingredients),
                manufacturer=Title(schema.manufacturer),
            ),
        )

    except ApplicationException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exc.message})

    return CreateProductResponseSchema(
        product_oid=product.oid,
        title=product.title,
        description=product.description,
        expiry_date=product.expiry_date,
        image_url=product.image_url,
        manufacturer=product.manufacturer,
        ingredients=product.ingredients,
    )


@router.post(
    '/delete-product',
    status_code=status.HTTP_204_NO_CONTENT,
    description="Эндпоинт удаления товара, если това не найден возвращается 400 ошибка",
)
async def delete_product(
    schema: DeleteProductRequestSchema,
    container=Depends(init_container),
):
    mediator: Mediator = container.resolve(Mediator)

    try:
        await mediator.handle_command(
            DeleteProductCommand(
                product_oid=schema.product_oid,
            ),
        )
    except ApplicationException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exc.message})

    return True


@router.post(
    '/search-product',
    status_code=status.HTTP_200_OK,
    description="Эндпоинт ищет товар с заданным названием от пользователя, если товара нет, возвращается 400 ошибка",
    responses={
        status.HTTP_201_CREATED: {'model': FindProductResponseSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema},
    },
)
async def search_product(
    schema: FindProductRequestSchema,
    container=Depends(init_container),
):
    mediator: Mediator = container.resolve(Mediator)
    try:
        products = await mediator.handle_command(
            FindProductCommand(
                product_title=schema.product_title,
            ),
        )
    except ApplicationException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exc.message})

    return FindProductResponseSchema(
        products=products,
    )
