from ostanes.utils import get_seesion


def test_core():
    assert 1 + 1 == 2


def test_simple_table_1(simple_table_1):
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
