from fastapi import APIRouter, Depends, HTTPException, status

from app.domain.exceptions.base import ApplicationException

from ....logic.commands.products import CreateProductCommand
from ....logic.init import init_container
from ....logic.mediator import Mediator
from ..schemas import ErrorSchema
from .schemas import CreateProductRequestSchema, CreateProductResponseSchema

router = APIRouter(tags=['/products'])


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
