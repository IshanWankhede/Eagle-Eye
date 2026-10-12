"""Centralized configuration loaded from environment variables / .env."""
from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "development"
    log_level: str = "INFO"
    cors_allowed_origins: str = "http://localhost:5173"
    database_url: str = "sqlite:///./artifacts/eagle_eye.sqlite3"
    upload_dir: str = "./artifacts/uploads"
    max_upload_mb: int = 25
    model_path: str = "./models/custom/best.pt"
    model_manifest_path: str = "./models/custom/model_manifest.json"
    detection_conf_threshold: float = 0.25
    detection_accept_threshold: float = 0.50

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_allowed_origins.split(",") if o.strip()]

    @property
    def model_file_exists(self) -> bool:
        return Path(self.model_path).is_file()


@lru_cache
def get_settings() -> Settings:
    return Settings()
