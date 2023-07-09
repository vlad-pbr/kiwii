"""
Base data layer class for instantiation by various components.
"""
from dataclasses import asdict
from json import dumps, loads
from pathlib import Path
from threading import Lock
from typing import Type, TypeVar, Optional, Dict

from kiwii.data.data_structures.datastructure import DataStructure
from kiwii.data.models.datalayer import DataLayer
from kiwii.shared.logging.componentloggername import ComponentLoggerName
from kiwii.shared.logging.logging import get_logger

_DataStructure = TypeVar("_DataStructure", bound=DataStructure)


class Data:

    def __init__(self, filepath: Path, component: ComponentLoggerName, log_level: str):

        # init properties
        self.lock = Lock()
        self.logger = get_logger(component)

        # set logging level
        self.logger.setLevel(log_level)

        # if path is relative - store in a dedicated home directory
        if not filepath.is_absolute():
            self.filepath: Path = Path.home() / ".kiwii" / filepath
        else:
            self.filepath: Path = filepath
        self.logger.debug(f"data will be persisted to '{self.filepath}'")

        # make sure parent directory exists
        self.filepath.parent.mkdir(parents=True, exist_ok=True)

        # if file does not already exist - write initial file
        if not self.filepath.is_file():
            with self.filepath.open(mode="w") as _file:
                # TODO overwrite
                _file.write(dumps(asdict(DataLayer())))

    def store(self, data_structure: _DataStructure) -> None:
        """Stores provided data structure to storage"""

        with self.lock:

            # read persisted data
            with self.filepath.open("r") as _file:
                data_layer: DataLayer = DataLayer(**loads(_file.read()))

            # update data with new structure
            data_layer.data_structures[data_structure.__class__.__name__] = data_structure

            # persist new data to file
            with self.filepath.open("w") as _file:
                _file.write(dumps(asdict(data_layer)))

    def retrieve(self, data_structure_type: Type[_DataStructure]) -> Optional[_DataStructure]:
        """Returns requested data structure or `None` if one is not currently present in storage"""

        with self.lock:

            # read persisted data
            with self.filepath.open("r") as _file:
                data_layer: DataLayer = DataLayer(**loads(_file.read()))

        # read data structure dictionary if one is present
        data_structure_dict: Optional[Dict] = data_layer.data_structures.get(data_structure_type.__name__, None)
        if data_structure_dict is None:
            return None

        # return underlying data structure
        return data_structure_type(**data_structure_dict)
