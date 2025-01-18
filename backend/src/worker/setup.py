from __future__ import annotations

from typing import Generic, Optional, TypeVar

import dramatiq
from dramatiq.brokers.rabbitmq import RabbitmqBroker
from dramatiq.results import Results
from dramatiq.results.backends.memcached import MemcachedBackend

from src.config import get_config

T = TypeVar("T")

ENGINE_KEY = "engine"
SESSIONMAKER_KEY = "sessionmaker"
OBJECT_STORE_KEY = "object-store-key"


class WorkerGlobal(Generic[T]):
    _container = {}
    _instance = None
    def __new__(cls) -> WorkerGlobal:
        if cls._instance is None:
            cls._instance = super(WorkerGlobal, cls).__new__(cls)
        return cls._instance
    def set(self, name: str, entity: T) -> None:
        self._container[name] = entity
    def get(self, name) -> Optional[T]:
        return self._container.get(name, None)


def setup_broker() -> None:
    config = get_config()
    broker = RabbitmqBroker(url=config.rabbitmq.get_amqp_uri())

    memcached_server = f"{config.worker.WORKER_MEMCACHED_HOST}:{config.worker.WORKER_MEMCACHED_PORT}"
    backend=MemcachedBackend(servers=[memcached_server], binary=True)
    broker.add_middleware(Results(backend=backend))

    dramatiq.set_broker(broker)


def close_broker() -> None:
    broker = dramatiq.get_broker()
    broker.close()
