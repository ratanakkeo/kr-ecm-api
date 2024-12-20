import os
from typing import Any, Optional
from pydantic import PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    @field_validator("SQLALCHEMY_DATABASE_URI", mode='before')
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], info: Any) -> Any:
        if isinstance(v, str):
            return v

        return PostgresDsn.build(
            scheme="postgresql",
            username=info.data.get("POSTGRES_USER"),
            password=info.data.get("POSTGRES_PASSWORD"),
            host=info.data.get("POSTGRES_SERVER"),
            port=int(info.data.get("POSTGRES_PORT", "5432")),
            path=f"/{info.data.get('POSTGRES_DB', '')}"
        )

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"

settings = Settings()
