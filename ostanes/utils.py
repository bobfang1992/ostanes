from contextlib import contextmanager
from typing import ContextManager

from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session


@contextmanager
def get_session(engine: Engine) -> ContextManager[Session]:
    session_maker = sessionmaker()
    session_maker.configure(bind=engine)
    session: Session = session_maker()
    yield session
    session.close()
