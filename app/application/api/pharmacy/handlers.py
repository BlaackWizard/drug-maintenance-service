from fastapi import APIRouter, Depends, HTTPException, status

from ....domain.exceptions.base import ApplicationException
from ....logic.commands.pharmacy import CreatePharmacyCommand
from ....logic.init import init_container
from ....logic.mediator import Mediator
from ..schemas import ErrorSchema
from .schemas import CreatePharmacyRequestSchema, CreatePharmacyResponseSchema

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
                title=schema.title,
                description=schema.description,
            ),
        )
    except ApplicationException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exc.message})

    return CreatePharmacyResponseSchema.from_entity(pharmacy)
