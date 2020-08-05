from ostanes.utils import get_session

def test_core():
    assert 1 + 1 == 2


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
    columns = user_table.columns
    assert len(columns) == 4
