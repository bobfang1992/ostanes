from abc import ABC, abstractmethod
from datetime import datetime
from typing import Collection, Mapping, Union

from sqlalchemy.schema import Column, Table
from sqlalchemy.sql.sqltypes import DateTime, Float, Integer, String

SQLValue = Union[int, str, float, datetime]
EnumValue = Collection[Union[int, str]]


class ColumnConfig(ABC):
    def __init__(self, column: Column):
        self._column = Column

    @abstractmethod
    def get_value(self) -> SQLValue:
        raise NotImplementedError("ColumnConfig is an abstract base class")


class EnumColumnConfig(ColumnConfig):
    def __init__(self, column, possible_values: EnumValue = None):
        self._column = column
        self.possible_values = possible_values

    def get_value(self) -> Union[int, str]:
        pass


class IntegerColumnConfig(ColumnConfig):
    def __init__(self, column, min_value=None, max_value=None):
        self._column = column
        self.min = min_value
        self.max = max_value

    def get_value(self) -> int:
        pass


class FloatColumnConfig(ColumnConfig):
    def __init__(self, column, min_value=None, max_value=None):
        self._column = column
        self.min = min_value
        self.max = max_value

    def get_value(self) -> int:
        pass


class StringColumnConfig(ColumnConfig):
    def __init__(self, column, template=None):
        self._column = column
        self.template = template

    def get_value(self) -> str:
        pass


class DateTimeColumnConfig(ColumnConfig):
    def __init__(self, column, min_value=None, max_value=None):
        self._column = column
        self.min_value = min_value
        self.max_value = max_value

    def get_value(self) -> datetime:
        pass


class PrimaryKeyColumnConfig(ColumnConfig):
    def __init__(self, column, col_type):
        self._column = column
        self.type = col_type

    def get_value(self):
        pass


class TableConfig:
    def __init__(
        self,
        table: Table,
        min_rows: int = None,
        max_rows: int = None,
        column_configs: Mapping[str, ColumnConfig] = None,
    ):
        self._min_rows = min_rows or 20
        self._max_rows = max_rows or 20
        self._table = table
        self._column_configs = column_configs

    @property
    def column_configs(self):
        return self._column_configs

    @property
    def table(self):
        return self._table


def generate_column_config(column: Column) -> ColumnConfig:
    col_type = type(column.type)
    if col_type == Integer:
        if column.primary_key:
            return PrimaryKeyColumnConfig(column, Integer)
        else:
            return IntegerColumnConfig(column)
    elif col_type == Float:
        return FloatColumnConfig(column)
    elif col_type == String:
        if column.primary_key:
            return PrimaryKeyColumnConfig(column, String)
        else:
            return StringColumnConfig(column)
    elif col_type == DateTime:
        return DateTimeColumnConfig(column)

    raise ValueError(f"Column {column} is not supported")


def generate_table_config(table: Table) -> TableConfig:
    columns = table.columns
    column_configs = {c.name: generate_column_config(c) for c in columns}
    table_config = TableConfig(table, column_configs=column_configs)
    return table_config
