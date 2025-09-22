from typing import List
from pydantic import BaseSettings, Field


Class Settings(BaseSettings):
"""App-wide settings loaded from environment variables."""

    uvicorn_host: str = Field("0.0.0.0", env="UVICORN_HOST")
    uvicorn_port: int = Field(8000, env="UVICORN_PORT")
    uvicorn_reload: bool = Field(True, env="UVICORN_RELOAD")

    # Required secret
    secret_key: str = Field(..., env="SECRET_KEY")

    # CORS
    cors_origins: List[str] = Field("*", env="CORS_ORIGINS")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"



# Singleton settings object
settings = Settings()