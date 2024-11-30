from fastapi import APIRouter, Depends, HTTPException, status

from ....domain.exceptions.base import ApplicationException
from ....domain.values.product import Text, Title
from ....logic.commands.pharmacy import (ChangeProductPriceCommand,
                                         CreatePharmacyCommand,
                                         DeletePharmacyCommand,
                                         DeleteProductFromPharmacyCommand,
                                         GetPharmacyByOidCommand,
                                         UpdatePharmacyCommand)
from ....logic.init import init_container
from ....logic.mediator import Mediator
from ..schemas import ErrorSchema
from .schemas import (ChangeProductPriceRequestSchema,
                      CreatePharmacyRequestSchema,
                      CreatePharmacyResponseSchema,
                      DeletePharmacyRequestSchema,
                      DeleteProductFromPharmacyRequestSchema,
                      UpdatePharmacyRequestSchema)

router = APIRouter(
    tags=['Pharmacy'],
)


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    description="Эндпоинт создает новую аптеку, если аптека с таким названием "
                "уже существует, то возвращается 400 ошибка",
    responses={
        status.HTTP_201_CREATED: {'model': CreatePharmacyResponseSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema},
    },
)
async def create_pharmacy_handler(schema: CreatePharmacyRequestSchema, container=Depends(init_container)):
    '''Создать новую аптеку'''
    mediator: Mediator = container.resolve(Mediator)

    try:
        pharmacy, *_ = await mediator.handle_command(
            CreatePharmacyCommand(
                title=Title(schema.title),
                description=Text(schema.description),
            ),
        )
    except ApplicationException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exc.message})

    return CreatePharmacyResponseSchema.from_entity(pharmacy)


@router.get(
    '/get-pharmacy',
    status_code=status.HTTP_200_OK,
    description="Эндпоинт ищет аптеку по oid, если его нет то возвращается 400 ошибка",
)
async def get_pharmacy_by_oid(
    pharmacy_oid: str,
    container=Depends(init_container),
):
    '''Ищет аптеку по oid'''
    mediator: Mediator = container.resolve(Mediator)
    try:
        pharmacy, *_ = await mediator.handle_command(
            GetPharmacyByOidCommand(
                pharmacy_oid=pharmacy_oid,
            ),
        )
    except ApplicationException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exc.message})

    return CreatePharmacyResponseSchema(
        oid=pharmacy.oid,
        title=pharmacy.title,
        description=pharmacy.description,
        products=pharmacy.products,
        prices=pharmacy.prices,
    )


@router.post(
    '/update-pharmacy',
    status_code=status.HTTP_202_ACCEPTED,
    description="Эндпоинт обновляет данные об аптеке",
)
async def update_pharmacy(
    pharmacy_oid: str,
    schema: UpdatePharmacyRequestSchema,
    container=Depends(init_container),
):
    '''Обновляет данные об аптеке'''
    mediator: Mediator = container.resolve(Mediator)

    try:

        pharmacy, *_ = await mediator.handle_command(
            UpdatePharmacyCommand(
                pharmacy_oid=pharmacy_oid,
                title=Title(schema.title),
                description=Text(schema.description),
            ),
        )
    except ApplicationException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exc.message})

    return CreatePharmacyResponseSchema(
        oid=pharmacy.oid,
        title=pharmacy.title,
        description=pharmacy.description,
        products=pharmacy.products,
        prices=pharmacy.prices,
    )


@router.post(
    '/change-price-product',
    description="Эндпоинт изменения цены товара из аптеки, если нет товара или аптеки то возвращается 400 ошибка",
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        status.HTTP_202_ACCEPTED: {'model': CreatePharmacyResponseSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema},
    },
)
async def change_price_product(
    schema: ChangeProductPriceRequestSchema,
    container=Depends(init_container),
):
    mediator: Mediator = container.resolve(Mediator)

    try:
        pharmacy, *_ = await mediator.handle_command(
            ChangeProductPriceCommand(
                pharmacy_oid=schema.pharmacy_oid,
                product_oid=schema.product_oid,
                price=schema.price,
            ),
        )
    except ApplicationException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exc.message})

    return CreatePharmacyResponseSchema(
        oid=pharmacy.oid,
        title=pharmacy.title,
        description=pharmacy.description,
        products=pharmacy.products,
        prices=pharmacy.prices,
    )


@router.post(
    '/delete-product-from-pharmacy',
    status_code=status.HTTP_204_NO_CONTENT,
    description="Эндпоинт удаления товара из аптеки, если товар или аптека не найдена, возвращается 400 ошибка",
)
async def delete_product_from_pharmacy(
    schema: DeleteProductFromPharmacyRequestSchema,
    container=Depends(init_container),
):
    mediator: Mediator = container.resolve(Mediator)

    try:
        await mediator.handle_command(
            DeleteProductFromPharmacyCommand(
                pharmacy_oid=schema.pharmacy_oid,
                product_oid=schema.product_oid,
            ),
        )
    except ApplicationException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exc.message})

    return True


@router.post(
    '/delete-pharmacy',
    status_code=status.HTTP_204_NO_CONTENT,
    description="Эндпоинт удаления аптеки, если аптека не найдена, возвращается 400 ошибка",
)
async def delete_pharmacy(
    schema: DeletePharmacyRequestSchema,
    container=Depends(init_container),
):
    mediator: Mediator = container.resolve(Mediator)

    try:
        await mediator.handle_command(
            DeletePharmacyCommand(
                pharmacy_oid=schema.pharmacy_oid,
            ),
        )
    except ApplicationException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exc.message})

    return True
