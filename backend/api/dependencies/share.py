from typing import Generator

from fastapi import Request
from sqlalchemy.orm import Session

from src.config import get_config
from src.objstore.base import BaseStore
from src.objstore.s3 import S3Store


def get_session(request: Request) -> Generator[Session, None, None]:
    sessionmaker = request.app.state.sessionmaker

    with sessionmaker() as session:
        try:
            yield session
        except Exception as exc:
            session.rollback()
            raise exc
        else:
            session.commit()


def get_object_store() -> BaseStore:
    config = get_config()
    store = S3Store(config.object_store)
    store.init()
    return store
