from fastapi import FastAPI


def create_app():
    return FastAPI(
        title="Pharmacy website",
        docs_url="/api/docs",
        description="Amazon s3 + ddd",
        debug=True,
    )
