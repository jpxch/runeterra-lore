from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field
from pathlib import Path
import os


class Settings(BaseSettings):
    """App-wide settings loaded from environment variables."""

    uvicorn_host: str = Field("0.0.0.0", env="UVICORN_HOST")
    uvicorn_port: int = Field(8000, env="UVICORN_PORT")
    uvicorn_reload: bool = Field(True, env="UVICORN_RELOAD")

    # Required secret
    secret_key: str = Field("dev-secret", env="SECRET_KEY")

    # CORS
    cors_origins: List[str] = Field(default=["*"], env="CORS_ORIGINS")

    # Data locations
    data_dir: Path = Path(os.getenv("DATA_DIR", Path(__file__).resolve().parents[1] / "data"))
    cache_dir: Path = Path(os.getenv("CACHE_DIR", Path(__file__).resolve().parents[1] / ".cache"))

    riot_api_base: str = Field("", env="RIOT_API_BASE")
    riot_api_key: str = Field("", env="RIOT_API_KEY")
    riot_default_locale: str = Field("en_US", env="RIOT_LOCALE")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"



# Singleton settings object
settings = Settings()
settings.cache_dir.mkdir(parents=True, exist_ok=True)