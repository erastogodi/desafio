# tests/conftest.py
import os
import pytest

# --- DEFINA AS ENVS ANTES DE IMPORTAR QUALQUER COISA DO app.* ---
os.environ.setdefault("APP_ENV", "test")
# permite sobrescrever via TEST_DATABASE_URL, senão usa localhost
os.environ["DATABASE_URL"] = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql+psycopg://app:app@localhost:5432/recipes_db",
)
os.environ.setdefault("JWT_SECRET", "test-secret")
os.environ.setdefault("ALLOWED_ORIGINS", "localhost:3000")
os.environ.setdefault("SUMMARIZER_BACKEND", "textrank")
# -----------------------------------------------------------------

from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

from app.models.base import Base
from app.core.db import engine, SessionLocal, get_db
from app.core.security import require_jwt
from app.main import create_app

# cria as tabelas uma vez por sessão
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    # opcional: limpar ao final
    # Base.metadata.drop_all(bind=engine)

# sessão de BD para cada teste
@pytest.fixture()
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# app com overrides de dependências
@pytest.fixture()
def app(db_session: Session):
    app = create_app()

    def _override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _override_get_db
    app.dependency_overrides[require_jwt] = lambda: "test-user"
    return app

# cliente HTTP
@pytest.fixture()
def client(app):
    return TestClient(app)
