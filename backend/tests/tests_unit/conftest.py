import tempfile

import pytest
from dramatiq.brokers.stub import StubBroker
from dramatiq.results import Results
from dramatiq.results.backends.stub import StubBackend
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session

from src.db.models import Base
from src.objstore.base import BaseStore
from src.objstore.file import FileStore


@pytest.fixture(autouse=True, scope="session")
def mock_dramatiq_broker() -> StubBroker:
    backend = StubBackend()
    broker = StubBroker(
        [
            Results(
                backend=backend
            )
        ]
    )
    broker.emit_after("process_boot")
    yield broker
    broker.close()


@pytest.fixture
def mock_db() -> Engine:
    engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)
    metadata = Base.metadata
    metadata.create_all(engine)
    yield engine
    metadata.drop_all(engine)


@pytest.fixture
def mock_session(mock_db) -> Session:
    return Session(mock_db)


@pytest.fixture
def mock_object_store() -> BaseStore:
    with tempfile.TemporaryDirectory() as tmp_dir:
         yield FileStore(tmp_dir)

