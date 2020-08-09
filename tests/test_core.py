from sqlalchemy.sql.sqltypes import Integer

from ostanes.generator import (
    generate_inserts_values_for_table,
    should_use_autoincrement_pkey,
)
from ostanes.tableconfig import (
    FloatColumnConfig,
    PrimaryKeyColumnConfig,
    generate_column_config,
    generate_table_config,
)
from ostanes.utils import get_session


def test_simple_table_1(simple_table_1):
    base = simple_table_1["sqlalchemy_base"]
    engine = simple_table_1["engine"]
    User = simple_table_1["tables"]["User"]
    assert engine is not None
    user_0 = User(name="bob", full_name="Bob Fang", nick_name="dorafmon")
    with get_session(engine) as s:
        s.add(user_0)
        s.commit()

    with get_session(engine) as s:
        all_users = s.query(User).all()
        assert len(all_users) == 1

    tables = base.metadata.tables
    assert len(tables) == 1
    assert list(tables.keys())[0] == "user"


def test_generate_column_config(simple_table_1):
    base = simple_table_1["sqlalchemy_base"]
    tables = base.metadata.tables
    user = tables["user"]
    columns = user.columns
    id_col = columns["id"]
    column_config = generate_column_config(id_col)
    assert isinstance(column_config, PrimaryKeyColumnConfig)
    assert column_config.type == Integer

    height_col = columns["height"]
    column_config = generate_column_config(height_col)
    assert isinstance(column_config, FloatColumnConfig)
    table_config = generate_table_config(user)
    column_configs = table_config.column_configs
    assert "id" in column_configs


def test_should_use_auto_increment_pkey(simple_table_1):
    base = simple_table_1["sqlalchemy_base"]
    tables = base.metadata.tables
    user = tables["user"]
    table_config = generate_table_config(user)
    auto_pkey = should_use_autoincrement_pkey(table_config)
    assert auto_pkey


def test_generate_inserts_for_table(simple_table_1):
    base = simple_table_1["sqlalchemy_base"]
    tables = base.metadata.tables
    user = tables["user"]
    table_config = generate_table_config(user)
    user_inserts_values = generate_inserts_values_for_table(table_config)
    engine = simple_table_1["engine"]
    engine.execute(user.insert(), user_inserts_values)

    with get_session(engine) as s:
        result = s.query(user).all()
        assert len(result) <= table_config.max_rows
        assert len(result) >= table_config.min_rows
