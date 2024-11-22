from fastapi import FastAPI

from .pharmacy.handlers import router as pharmacy_router
from .products.handlers import router as product_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Pharmacy website",
        docs_url="/api/docs",
        description="Amazon s3 + ddd",
        debug=True,
    )
    app.include_router(pharmacy_router, prefix='/pharmacy')
    app.include_router(product_router, prefix='/products')

    return app
