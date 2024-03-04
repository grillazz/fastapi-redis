from fastapi import Depends, FastAPI

from app.config import  settings
from app.logging import AppLogger
from app.redis import init_redis_pool
from app.routers import smiles_router
from app.service import MoleculesRepository
from app.config import settings as global_settings

logger = AppLogger().get_logger()

app = FastAPI(title="ChemCompoundsAPI", version="0.0.0")
app.include_router(smiles_router)


@app.on_event("startup")
async def startup_event():
    logger.info("Opening mols bakery...")
    app.state.redis = await init_redis_pool()
    app.state.mols_repo = MoleculesRepository(app.state.redis)


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Closing mols bakery...")
    await app.state.redis.close()


@app.get("/health-check")
async def health_check():
    try:
        await app.state.redis.set(str(settings.redis_url), settings.up)
        value = await app.state.redis.get(str(settings.redis_url))
    except Exception:  # noqa: E722
        logger.exception("Sorry no power we can't open bakery...")
        value = settings.down
    return {settings.web_server: settings.up, str(settings.redis_url): value}
