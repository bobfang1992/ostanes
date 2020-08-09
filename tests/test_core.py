from sqlalchemy.sql.sqltypes import Integer

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

    user_table = tables["user"]
    user_table.columns


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
