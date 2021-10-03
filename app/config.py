import os
from functools import lru_cache

from pydantic import AnyUrl, BaseSettings

from app.utils import get_logger

logger = get_logger(__name__)


class Settings(BaseSettings):
    environment: str = os.getenv("ENVIRONMENT", "dev")
    testing: str = os.getenv("TESTING", "0")
    redis_url: AnyUrl = os.environ.get("REDIS_URL", "redis://redis")
    redis_password: str = os.getenv("REDIS_PASSWORD", "redis_pass")
    redis_db: int = int(os.getenv("REDIS_DB", "0"))
    redis_hash: str = os.getenv("REDIS_TEST_KEY", "covid-19-test")
    up: str = os.getenv("UP", "up")
    down: str = os.getenv("DOWN", "down")
    web_server: str = os.getenv("WEB_SERVER", "web_server")


@lru_cache
def get_settings() -> BaseSettings:
    logger.info("Loading config settings from the environment...")
    return Settings()
