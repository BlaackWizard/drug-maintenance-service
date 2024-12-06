from app.logic.commands.pharmacy import (AddProductWithPriceHandler,
                                         ChangeProductPriceHandler,
                                         DeletePharmacyHandler,
                                         DeleteProductFromPharmacyHandler,
                                         FindPharmacyHandler,
                                         GetPharmacyByOidHandler,
                                         PharmacyHandler,
                                         UpdatePharmacyHandler)
from app.logic.commands.products import (CreateProductCommandHandler,
                                         DeleteProductHandler,
                                         FindProductHandler,
                                         GetProductByOidHandler,
                                         UpdateProductHandler)


def init_handler_dependencies(container):
    container.register(CreateProductCommandHandler)
    container.register(PharmacyHandler)
    container.register(GetProductByOidHandler)
    container.register(GetPharmacyByOidHandler)
    container.register(UpdatePharmacyHandler)
    container.register(UpdateProductHandler)
    container.register(ChangeProductPriceHandler)
    container.register(AddProductWithPriceHandler)
    container.register(DeleteProductFromPharmacyHandler)
    container.register(DeleteProductHandler)
    container.register(DeletePharmacyHandler)
    container.register(FindProductHandler)
    container.register(FindPharmacyHandler)
