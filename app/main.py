# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.db import engine
from app.models.base import Base

from app.routers.status import router as status_router
from app.routers.auth_router import router as auth_router
from app.routers.importar import router as importar_router
from app.routers.receitas import router as receitas_router
from app.routers.indicadores import router as indicadores_router

def create_app() -> FastAPI:
    app = FastAPI(
        title="Recipes API",
        version="0.3.0",
        description="API de receitas baseada em TheMealDB — importação, listagem e indicadores.",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )

    @app.on_event("startup")
    def _init_db() -> None:
        Base.metadata.create_all(bind=engine)

    app.include_router(status_router, tags=["Status"])
    app.include_router(auth_router, tags=["Auth"])
    app.include_router(importar_router, tags=["Importação"])
    app.include_router(receitas_router, tags=["Receitas"])
    app.include_router(indicadores_router, tags=["Indicadores"])
    return app

app = create_app()
