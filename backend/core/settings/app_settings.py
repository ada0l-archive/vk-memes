import logging
import sys

from loguru import logger
from pydantic import BaseSettings

from backend.core.logging import InterceptHandler
from backend.core.settings.app_env_types import AppEnvTypes


class BaseAppSettings(BaseSettings):
    app_env: AppEnvTypes = AppEnvTypes.test

    class Config:
        env_file = ".env"


class AppSettings(BaseAppSettings):
    debug: bool = False
    docs_url: str = "/docs"
    openapi_prefix: str = ""
    openapi_url: str = "/openapi.json"
    redoc_url: str = "/redoc"
    title: str = "Application"
    version: str = "0.0.0"

    database_url: str

    secret_key: str
    allowed_hosts: list[str] = ["*"]

    logging_hosts: int = logging.INFO
    logging_level = logging.INFO
    loggers: tuple[str, str] = ("uvicorn.asgi", "uvicorn.access")

    installed_apps = [
        "backend.mem",
    ]

    models = []
    for app in installed_apps:
        from importlib.util import find_spec
        model_file = f"{app}.models"
        try:
            find_spec(model_file)
            found = True
        except ModuleNotFoundError:
            found = False
        if found:
            models.append(model_file)

    class Config:
        validate_assigment = True

    @property
    def fastapi_kwargs(self) -> dict[str, any]:
        return {
            "debug": self.debug,
            "docs_url": self.docs_url,
            "openapi_url": self.openapi_url,
            "redoc_url": self.redoc_url,
            "title": self.title,
            "version": self.version,
        }

    def configure_logging(self) -> None:
        logging.getLogger().handlers = [InterceptHandler()]
        for logger_name in self.loggers:
            logging_logger = logging.getLogger(logger_name)
            logging_logger.handlers = [InterceptHandler(level=self.logging_level)]

        logger.configure(handlers=[{"sink": sys.stderr, "level": self.logging_level}])


class DevAppSettings(AppSettings):
    debug: bool = True

    title: str = "Dev Application"

    logging_level: int = logging.DEBUG

    class Config(AppSettings.Config):
        env_file = ".env.dev"


class ProdAppSettings(AppSettings):
    class Config(AppSettings.Config):
        env_file = ".env.prod"


class TestAppSettings(AppSettings):
    debug: bool = True

    title: str = "Test Application"

    secret_key: str = "test"

    logging_level: int = logging.DEBUG

    class Config(AppSettings.Config):
        env_file = ".env.test"
