from typing import Optional

from sqlalchemy import Engine, create_engine, text
from sqlalchemy.orm import sessionmaker

from src.config import get_config
from src.db.models import Base

drop_table_statement = """
DROP SCHEMA IF EXISTS main CASCADE;
CREATE SCHEMA main;"""


def get_engine() -> Engine:
    config = get_config()
    user = config.postgres.POSTGRES_USER
    password = config.postgres.POSTGRES_PASSWORD
    host = config.postgres.POSTGRES_HOST
    port = config.postgres.POSTGRES_PORT
    database_name = config.postgres.POSTGRES_DB

    postgres_url = f"postgresql://{user}:{password.get_secret_value()}@{host}:{port}/{database_name}"
    engine = create_engine(postgres_url)
    return engine


def get_sessionmaker(engine: Engine) -> sessionmaker:
    return sessionmaker(engine)


def init(engine: Optional[Engine] = None) -> None: # type: ignore
    if engine is None:
        engine = get_engine()
    metadata = Base.metadata

    with engine.connect() as conn:
        conn.execute(text(drop_table_statement))
        conn.commit()

    metadata.create_all(engine)


if __name__ == "__main__":
    import time

    retries = 5
    while True:
        try:
            init()
            break
        except Exception as exc:
            print("An error happening")
            retries -= 1

            if retries == 0:
                raise exc

            time.sleep(5)
