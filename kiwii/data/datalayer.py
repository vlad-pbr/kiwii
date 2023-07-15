from __future__ import annotations

from dataclasses import dataclass, field, fields, asdict, is_dataclass
from importlib import import_module
from json import dumps, loads
from typing import Dict, Type, get_type_hints, Union, Optional

from kiwii.data.data_structures.datastructure import DataStructure
from kiwii.data.types import TDataStructure


@dataclass
class DataLayer:
    """
    Top level data container which stores underlying data structures in a dictionary.

    In order to be able to serialize and deserialize a data layer, the following rules and limitations must apply:
    - Only primitive types, lists, dicts, tuples and dataclasses are supported
    - All fields must be typed
    - Non-primitive types must use `typing` types
    - In order to nest complex data structures, dataclasses must be used
    - Dictionary key types must be builtins, values can be dataclasses
    - Dictionary value types must not be nested, use dataclasses instead
    """

    data_structures: Dict[str, DataStructure] = field(default_factory=dict)

    def retrieve(self, data_structure_type: Type[TDataStructure]) -> Optional[TDataStructure]:
        """Returns requested data structure or `None` if one is not currently present in the data layer."""

        return self.data_structures.get(self._get_fqn(data_structure_type), None)

    def store(self, data_structure: TDataStructure) -> None:
        """Stores provided data structure to data layer."""

        self.data_structures[self._get_fqn(data_structure.__class__)] = data_structure

    def serialize(self) -> str:
        """Serializes current `DataLayer` object to JSON string."""

        return dumps(asdict(self)[fields(self)[0].name])

    @classmethod
    def deserialize(cls, data: str) -> DataLayer:
        """Deserializes provided JSON string data into a complete `DataLayer` object."""

        # parse JSON string as-is
        data_dict: Dict[str, Union[Dict, object]] = loads(data)

        # semantically parse all data structures within parsed JSON
        for data_structure_module_name, data_structure_data_dict in data_dict.items():
            data_dict[data_structure_module_name] = \
                cls._data_to_dataclass(data_structure_data_dict, data_structure_module_name)

        # return fully parsed instance of DataLayer
        return cls(**{fields(cls)[0].name: data_dict})

    @classmethod
    def _data_to_dataclass(cls, data: Dict, fqn: str) -> object:
        """Recursively parses `data` dictionary to a dataclass instance specified in `fqn`."""

        # dynamically import target dataclass
        fqn_split = fqn.split(".")
        module_name, package_name = ".".join(fqn_split[:-1]), fqn_split[-1]
        target_dataclass = import_module(name=module_name).__dict__[package_name]

        # handle each field within dataclass
        target_dataclass_typehints = get_type_hints(target_dataclass)
        for _field in fields(target_dataclass):

            _field_type = target_dataclass_typehints[_field.name]

            # handle dataclass
            if is_dataclass(_field_type):
                data[_field.name] = cls._data_to_dataclass(data[_field.name], cls._get_fqn(_field_type))

            # handle list of dataclasses
            elif _field_type.__name__.startswith("List"):

                # fetch the typing list item type and if it's a dataclass - parse
                _field_builder = _field_type.__args__[0]
                if is_dataclass(_field_builder):
                    data[_field.name] = [
                        cls._data_to_dataclass(_field_data, cls._get_fqn(_field_builder))
                        for _field_data in data[_field.name]
                    ]

            # handle dictionary where value type is dataclass
            elif _field_type.__name__.startswith("Dict"):

                # fetch teh typing dictionary value type and if it's a dataclass - parse
                _field_builder = _field_type.__args__[1]
                if is_dataclass(_field_builder):
                    data[_field.name] = {
                        k: cls._data_to_dataclass(v, cls._get_fqn(_field_builder))
                        for k, v in data[_field.name].items()
                    }

        return target_dataclass(**data)

    @staticmethod
    def _get_fqn(_type: Type) -> str:
        """Returns fully qualified name of a class."""

        return f"{_type.__module__}.{_type.__qualname__}"
