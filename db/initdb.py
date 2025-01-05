from db.model import Base
from sqlalchemy import create_engine, text, Engine
from config import get_config

schemas = ["main"]
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


def init() -> None:
    engine = get_engine()
    metadata = Base.metadata

    with engine.connect() as conn:
        conn.execute(text(drop_table_statement))
        conn.commit()
    metadata.create_all(engine)


if __name__ == "__main__":
    init()
