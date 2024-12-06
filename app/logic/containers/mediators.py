from app.logic.commands.pharmacy import PharmacyHandler, CreatePharmacyCommand, GetPharmacyByOidCommand, \
    GetPharmacyByOidHandler, UpdatePharmacyCommand, UpdatePharmacyHandler, ChangeProductPriceCommand, \
    ChangeProductPriceHandler, AddProductWithPriceCommand, AddProductWithPriceHandler, DeleteProductFromPharmacyCommand, \
    DeleteProductFromPharmacyHandler, DeletePharmacyCommand, DeletePharmacyHandler, FindPharmacyCommand, \
    FindPharmacyHandler
from app.logic.commands.products import CreateProductCommand, GetProductByOidCommand, GetProductByOidHandler, \
    UpdateProductCommand, UpdateProductHandler, DeleteProductCommand, DeleteProductHandler, FindProductCommand, \
    FindProductHandler, CreateProductCommandHandler


def register_mediator_commands(container, mediator):
    mediator.register_command(
        CreatePharmacyCommand,
        [container.resolve(PharmacyHandler)],
    )
    mediator.register_command(
        CreateProductCommand,
        [container.resolve(CreateProductCommandHandler)],
    )
    mediator.register_command(
        GetProductByOidCommand,
        [container.resolve(GetProductByOidHandler)],
    )
    mediator.register_command(
        GetPharmacyByOidCommand,
        [container.resolve(GetPharmacyByOidHandler)],
    )
    mediator.register_command(
        UpdatePharmacyCommand,
        [container.resolve(UpdatePharmacyHandler)],
    )
    mediator.register_command(
        UpdateProductCommand,
        [container.resolve(UpdateProductHandler)],
    )
    mediator.register_command(
        ChangeProductPriceCommand,
        [container.resolve(ChangeProductPriceHandler)],
    )
    mediator.register_command(
        AddProductWithPriceCommand,
        [container.resolve(AddProductWithPriceHandler)],
    )
    mediator.register_command(
        DeleteProductFromPharmacyCommand,
        [container.resolve(DeleteProductFromPharmacyHandler)],
    )
    mediator.register_command(
        DeleteProductCommand,
        [container.resolve(DeleteProductHandler)],
    )
    mediator.register_command(
        DeletePharmacyCommand,
        [container.resolve(DeletePharmacyHandler)],
    )
    mediator.register_command(
        FindProductCommand,
        [container.resolve(FindProductHandler)]
    )
    mediator.register_command(
        FindPharmacyCommand,
        [container.resolve(FindPharmacyHandler)]
    )
    return mediator