import random
import string
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Collection, List, Mapping, Optional, Union

from sqlalchemy.schema import Column, Table
from sqlalchemy.sql.sqltypes import DateTime, Float, Integer, String

SQLValue = Union[int, str, float, datetime]
SQLValueList = Union[List[int], List[str], List[float], List[datetime]]
EnumValue = Collection[Union[int, str]]


def generate_random_date_between_dates(start, end):
    """
    Generate random datetime between two datestime
    Args:
        start: start datetime
        end: end datetime

    Returns:
        A random datetime object between the time range
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)


def generate_totally_random_string(length: int, alphabet: Optional[str] = None) -> str:
    """
    Generate a random string, chars are drawn from alphabet, length must be explicitly
    set
    Args:
        length: int
        alphabet: defaulted to uppercase ASCII and digits.
    Returns:
        random string with length
    """
    alphabet = alphabet or string.ascii_uppercase + string.digits
    return "".join(random.choices(alphabet, k=length))


class ColumnConfig(ABC):
    def __init__(self, column: Column):
        self._column = Column

    @abstractmethod
    def get_values(self, row: int) -> SQLValueList:
        raise NotImplementedError("ColumnConfig is an abstract base class")

    def is_primary_key(self):
        return False

    def __repr__(self):
        return f"{self.__class__.__name__}(column={self._column})"


class EnumColumnConfig(ColumnConfig):
    def __init__(self, column, possible_values: EnumValue = None):
        super().__init__(column)
        self.possible_values = possible_values

    def get_values(self, row: int) -> Union[List[int], List[str]]:
        pass


class IntegerColumnConfig(ColumnConfig):
    def __init__(self, column, min_value=None, max_value=None):
        super().__init__(column)
        self.min = min_value or 0
        self.max = max_value or 100

    def get_values(self, row) -> List[int]:
        result = []
        for i in range(row):
            result.append(random.randint(self.min, self.max))
        return result


class FloatColumnConfig(ColumnConfig):
    def __init__(self, column, min_value=None, max_value=None):
        super().__init__(column)
        self.min = min_value or -10
        self.max = max_value or 10

    def get_values(self, row) -> List[float]:
        result = []
        for i in range(row):
            result.append(random.uniform(self.min, self.max))
        return result


class StringColumnConfig(ColumnConfig):
    def __init__(self, column, template=None):
        super().__init__(column)
        self.template = template
        self._default_length = 5

    def get_values(self, row) -> List[str]:
        result = []
        for i in range(row):
            result.append(generate_totally_random_string(self._default_length))
        return result


class DateTimeColumnConfig(ColumnConfig):
    def __init__(self, column, min_value=None, max_value=None):
        super().__init__(column)
        self.min_value = min_value or datetime(1990, 1, 1)
        self.max_value = max_value or datetime(2019, 12, 31)

    def get_values(self, row) -> List[datetime]:
        result = []
        for i in range(row):
            result.append(
                generate_random_date_between_dates(self.min_value, self.max_value)
            )
        return result


class PrimaryKeyColumnConfig(ColumnConfig):
    def __init__(self, column, col_type):
        super().__init__(column)
        self.type = col_type

    @property
    def col_type(self):
        return self.type

    def get_values(self, row: int) -> Union[List[int], List[str]]:
        pass

    def is_primary_key(self):
        return True


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

    @property
    def min_rows(self):
        return self._min_rows

    @property
    def max_rows(self):
        return self._max_rows


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
