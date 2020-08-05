from ostanes.utils import get_columns, get_seesion, get_tables


def test_core():
    assert 1 + 1 == 2


def test_simple_table_1(simple_table_1):
    base = simple_table_1["sqlalchemy_base"]
    engine = simple_table_1["engine"]
    User = simple_table_1["tables"]["User"]
    assert engine is not None
    user_0 = User(name="bob", full_name="Bob Fang", nick_name="dorafmon")
    with get_seesion(engine) as s:
        s.add(user_0)
        s.commit()

    with get_seesion(engine) as s:
        all_users = s.query(User).all()
        assert len(all_users) == 1

    tables = get_tables(meta=base.metadata)
    assert len(tables) == 1
    assert list(tables.keys())[0] == "user"

    user_table = tables["user"]
    columns = get_columns(user_table)
    assert len(columns) == 4
