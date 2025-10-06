from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Configurações globais do backend — carregadas a partir de variáveis de ambiente (.env)
    ou valores padrão (para desenvolvimento local).
    """

    # ============================
    # 🔹 Banco de Dados
    # ============================
    DATABASE_URL: str

    # ============================
    # 🔹 JWT / Autenticação
    # ============================
    JWT_SECRET: str = "supersecretkey"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRES_MIN: int = 60  # duração do token (minutos)

    # ============================
    # 🔹 CORS
    # ============================
    ALLOWED_ORIGINS: str = "http://localhost:3000"

    # ============================
    # 🔹 Docker / Orquestração
    # ============================
    API_KEY: str | None = None
    SUMMARIZER_BACKEND: str | None = None

    # ============================
    # 🔹 Tradução automática
    # ============================
    TRANSLATE_TO_PT: bool = True  

    # ============================
    # 🔹 Outras opções gerais
    # ============================
    DEBUG: bool = True
    PROJECT_NAME: str = "Recipes API"
    VERSION: str = "0.3.0"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Instância global
settings = Settings()
