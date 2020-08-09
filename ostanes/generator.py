import random
from typing import Dict, List

from sqlalchemy.sql.sqltypes import Integer

from ostanes.tableconfig import TableConfig


def should_use_autoincrement_pkey(table_config: TableConfig):
    column_configs = table_config.column_configs

    primary_keys = []
    for c_config in column_configs.values():
        if c_config.is_primary_key():
            primary_keys.append(c_config)

    """
    This is a very rough check and may not be suitable but I will
    user it for now
    TODO: think more about this:
    https://groups.google.com/g/sqlalchemy/c/o5YQNH5UUko
    """
    should_use_auto_increment_primary_key = (
        len(primary_keys) == 1 and primary_keys[0].col_type == Integer
    )
    return should_use_auto_increment_primary_key


def dict_of_arrays_to_array_of_dicts(d: dict) -> list:
    v = [dict(zip(d, t)) for t in zip(*d.values())]
    return v


def generate_inserts_values_for_table(table_config: TableConfig) -> List[Dict]:
    """
    """
    # table = table_config.table
    auto_pkey = should_use_autoincrement_pkey(table_config)
    assert (
        auto_pkey
    ), "for now let's assume we are using only auto-incrementing integer pkeys"
    column_configs = table_config.column_configs

    if auto_pkey:
        value_columns = {
            key: column_configs[key]
            for key in column_configs
            if not column_configs[key].is_primary_key()
        }
    else:
        value_columns = {key: column_configs[key] for key in column_configs}
    values = {}
    rows = random.randint(table_config.min_rows, table_config.max_rows)
    for key in value_columns:
        values[key] = value_columns[key].get_values(rows)
    return dict_of_arrays_to_array_of_dicts(values)
