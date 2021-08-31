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
    use_redis_sentinel: bool = True if os.getenv("REDIS_USE_SENTINEL", "0") == "1" else False
    redis_sentinel_port: int = int(os.getenv("REDIS_SENTINEL_PORT", "26379"))
    redis_sentinel_url: str = os.getenv("REDIS_SENTINEL_URL", "")
    redis_sentinel_password: str = os.getenv("REDIS_SENTINEL_PASSWORD", "")
    redis_sentinel_master_name: str = os.getenv("REDIS_SENTINEL_MASTER_NAME", "molmaster")
    up: str = os.getenv("UP", "up")
    down: str = os.getenv("DOWN", "down")
    web_server: str = os.getenv("WEB_SERVER", "web_server")


@lru_cache()
def get_settings() -> BaseSettings:
    logger.info("Loading config settings from the environment...")
    return Settings()
