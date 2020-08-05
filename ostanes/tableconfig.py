from abc import ABC, abstractmethod
from datetime import datetime
from typing import Collection, Mapping, Union

SQLValue = Union[int, str, float, datetime]
EnumValue = Collection[Union[int, str]]


class ColumnConfig(ABC):
    @abstractmethod
    def get_value(self) -> SQLValue:
        raise NotImplementedError("ColumnConfig is an abstract base class")


class EnumColumnConfig(ColumnConfig):
    def __init__(self, possible_values: EnumValue = None):
        self.possible_values = possible_values

    def get_value(self) -> Union[int, str]:
        pass


class IntegerColumnConfig(ColumnConfig):
    def __init__(self, min_value=None, max_value=None):
        self.min = min_value
        self.max = max_value

    def get_value(self) -> int:
        pass


class FloatColumnConfig(ColumnConfig):
    def __init__(self, min_value=None, max_value=None):
        self.min = min_value
        self.max = max_value

    def get_value(self) -> int:
        pass


class StringColumnConfig(ColumnConfig):
    def __init__(self, template=None):
        self.template = template

    def get_value(self) -> str:
        pass


class DateTimeColumnConfig(ColumnConfig):
    def __init__(self, min_value=None, max_value=None):
        self.min_value = min_value
        self.max_value = max_value

    def get_value(self) -> datetime:
        pass


class TableConfig:
    def __init__(
        self,
        min_rows: int = None,
        max_rows: int = None,
        column_configs: Mapping[str, ColumnConfig] = None,
    ):
        self._min_rows = min_rows
        self._max_rows = max_rows
        self._column_configs = column_configs
