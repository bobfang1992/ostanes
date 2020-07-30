from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Collection, Mapping, Optional, Union

SQLValue = Union[int, str, float, datetime]
EnumValue = Collection[Union[int, str]]


class ColumnConfig(ABC):
    @abstractmethod
    def get_value(self) -> SQLValue:
        raise NotImplementedError("ColumnConfig is an abstract base class")


class EnumColumnConfig(ColumnConfig):
    def __init__(self, possible_values: EnumValue):
        self.possible_values = possible_values

    def get_value(self) -> Union[int, str]:
        pass


class IntegerColumnConfig(ColumnConfig):
    def __init__(self, min_value, max_value):
        self.min = min_value
        self.max = max_value

    def get_value(self) -> int:
        pass


class StringColumnConfig(ColumnConfig):
    def __init__(self, template):
        self.template = template

    def get_value(self) -> str:
        pass


class DateTimeColumnConfig(ColumnConfig):
    def __init__(self, min_value, max_value):
        self.min_value = min_value
        self.max_value = max_value

    def get_value(self) -> datetime:
        pass


@dataclass
class TableConfig:
    row: int = 20
    columns: Optional[Mapping[str, ColumnConfig]] = None
