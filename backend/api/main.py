import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.events.db import close_db_state, create_db_state
from api.middlewares import ExceptionMiddleware
from api.routes.metrics import router as metric_router
from api.routes.reference import router as reference_router
from api.routes.sample import router as sample_router
from src.config import get_config
from src.logger import init_logger, logger


def lifespan(app: FastAPI):
    config = get_config()
    init_logger(config.LOG_LEVEL)

    logger.info("BioValidator have been starting up")
    create_db_state(app)

    yield

    logger.info("BioValidator have started to shutdown")
    close_db_state(app)


app = FastAPI(
    title='BioValidator API',
    description='BioValidator API',
    docs_url='/docs',
    openapi_url='/openapi.json',
    lifespan=lifespan,
)

app.add_middleware(ExceptionMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(sample_router)
app.include_router(reference_router)
app.include_router(metric_router)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
