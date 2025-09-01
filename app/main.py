from __future__ import annotations
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from .database import Base, engine
from .routers import auth as auth_router, books as books_router

# Kreiranje tablica pri startu
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library API", version="1.0.0")

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Library API",
        version="1.0.0",
        description="API za evidenciju knjiga (FastAPI + MySQL + Redis)",
        routes=app.routes,
    )
    # osiguraj da 'components' postoji
    if "components" not in openapi_schema:
        openapi_schema["components"] = {}
    if "securitySchemes" not in openapi_schema["components"]:
        openapi_schema["components"]["securitySchemes"] = {}

    # definiraj Bearer JWT shemu
    openapi_schema["components"]["securitySchemes"]["HTTPBearer"] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
    }

    # globalni security zahtjev (pojavljuje Authorize gumb)
    openapi_schema["security"] = [{"HTTPBearer": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Routeri
app.include_router(auth_router.router)
app.include_router(books_router.router)

@app.get("/", tags=["health"])
def health():
    return {"status": "ok"}
