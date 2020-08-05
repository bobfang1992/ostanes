from contextlib import contextmanager
from typing import ContextManager

from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.schema import MetaData, Table


@contextmanager
def get_seesion(engine: Engine) -> ContextManager[Session]:
    session_maker = sessionmaker()
    session_maker.configure(bind=engine)
    session = session_maker()
    yield session
    session.close()


def get_tables(meta: MetaData):
    return meta.tables


def get_columns(table: Table):
    return table.columns
