import pytest
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

SQLLITE_IN_MEMORY = "sqlite:///:memory:"


@pytest.fixture
def new_base():
    Base = declarative_base()
    return Base


@pytest.fixture
def sqlite_engine():
    engine = create_engine(SQLLITE_IN_MEMORY)
    return engine


@pytest.fixture
def simple_table_1(new_base, sqlite_engine):
    Base = new_base
    engine = sqlite_engine

    class User(Base):
        __tablename__ = "user"

        id = Column(Integer, primary_key=True)
        name = Column(String)
        full_name = Column(String)
        nick_name = Column(String)

    Base.metadata.create_all(engine)

    return {"sqlalchemy_base": Base, "engine": engine, "tables": {"User": User}}
