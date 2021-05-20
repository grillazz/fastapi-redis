from fastapi import Depends, FastAPI
from fastapi import FastAPI, applications
from fastapi.openapi.docs import get_swagger_ui_html

from app import config
from app.redis import init_redis_pool
from app.routers import smiles_router
from app.service import MoleculesRepository

def swagger_monkey_patch(*args, **kwargs):
    """
    Wrap the function which is generating the HTML for the /docs endpoint and
    overwrite the default values for the swagger js and css.
    """
    return get_swagger_ui_html(
        *args,
        **kwargs,
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@3.48.0/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@3.48.0/swagger-ui.css"
    )


# Actual monkey patch
applications.get_swagger_ui_html = swagger_monkey_patch

global_settings = config.Settings()


app = FastAPI(title="ChemCompoundsAPI", version="0.1")
app.include_router(smiles_router, prefix="/api/smiles")


@app.on_event("startup")
async def startup_event():
    app.state.redis = await init_redis_pool()
    app.state.mols_repo = MoleculesRepository(app.state.redis)


@app.on_event("shutdown")
async def shutdown_event():
    app.state.redis.close()
    await app.state.redis.wait_closed()


@app.get("/health-check")
async def health_check(settings: config.Settings = Depends(config.get_settings)):
    try:
        await app.state.redis.set(str(settings.redis_url), settings.up)
        value = await app.state.redis.get(str(settings.redis_url))
    except:  # noqa: E722
        value = settings.down
    return {settings.web_server: settings.up, str(settings.redis_url): value}
