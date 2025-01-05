from fastapi import FastAPI

from src.db.initdb import get_engine, get_sessionmaker


def create_db_state(app: FastAPI) -> None:
    engine = get_engine()
    sessionmaker = get_sessionmaker(engine)

    app.state.engine = engine
    app.state.sessionmaker = sessionmaker


def close_db_state(app: FastAPI) -> None:
    if getattr(app.state, "engine", None) is not None:
        app.state.engine.dispose()
