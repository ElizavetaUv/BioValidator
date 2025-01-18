from src.config import get_config
from src.db.initdb import get_engine, get_sessionmaker
from src.logger import init_logger
from src.objstore.s3 import S3Store
from src.worker.setup import ENGINE_KEY, OBJECT_STORE_KEY, SESSIONMAKER_KEY, WorkerGlobal, setup_broker

config = get_config()

engine = get_engine()
sessionmaker = get_sessionmaker(engine)

object_store = S3Store(config.object_store)

worker_global = WorkerGlobal()

worker_global.set(ENGINE_KEY, engine)
worker_global.set(SESSIONMAKER_KEY, sessionmaker)
worker_global.set(OBJECT_STORE_KEY, object_store)

init_logger(config.LOG_LEVEL)

setup_broker()

from src.worker.tasks import *
