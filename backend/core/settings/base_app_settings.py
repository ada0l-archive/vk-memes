from pydantic import BaseSettings

from backend.core.settings.app_env_types import AppEnvTypes


class BaseAppSettings(BaseSettings):
    app_env: AppEnvTypes = AppEnvTypes.test

    class Config:
        env_file = ".env"
