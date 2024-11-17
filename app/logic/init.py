from .mediator import Mediator
from .commands.pharmacy import CreatePharmacyCommand, PharmacyHandler
from ..infra.repositories.pharmacy import BasePharmacyRepo


def init_mediator(
    mediator: Mediator,
    pharmacy_repo: BasePharmacyRepo
):
    mediator.register_command(
        CreatePharmacyCommand,
        [PharmacyHandler(pharmacy_repo=pharmacy_repo)],
    )