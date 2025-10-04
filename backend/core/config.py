from typing import List
from pathlib import Path
try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """App-wide settings loaded from environment variables."""

    uvicorn_host: str = Field(default="0.0.0.0", env="UVICORN_HOST")
    uvicorn_port: int = Field(default=8000, env="UVICORN_PORT")
    uvicorn_reload: bool = Field(default=True, env="UVICORN_RELOAD")

    # Required secret
    secret_key: str = Field(default="dev-secret", env="SECRET_KEY")

    # CORS
    cors_origins: List[str] = Field(default=["*"], env="CORS_ORIGINS")

    # Data locations
    data_dir: Path = Field(default=Path("data"), env="DATA_DIR")
    cache_dir: Path = Field(default=Path(".cache"), env="CACHE_DIR")

    riot_api_base: str = Field(default="https://ddragon.leagueoflegends.com/cdn/", env="RIOT_API_BASE")
    riot_default_locale: str = Field(default="en_US", env="RIOT_LOCALE")

    db_host: str = Field(default="localhost", env="DB_HOST")
    db_port: int = Field(default=5432, env="DB_PORT")
    db_name: str = Field(default="runeterra", env="DB_NAME")
    db_user: str = Field(default="runeterra", env="DB_USER")
    db_pass: str = Field(default="password", env="DB_PASS")

    vite_api_url: str = Field(default="/api", env="VITE_API_URL")

    class Config:
        env_file = "keys.env"
        env_file_encoding = "utf-8"
        extra = "ignore"



# Singleton settings object
settings = Settings()
settings.cache_dir.mkdir(parents=True, exist_ok=True)