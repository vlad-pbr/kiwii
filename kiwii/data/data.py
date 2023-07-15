"""
Base data layer class for instantiation by various components.
"""

from pathlib import Path
from threading import Lock
from typing import Type, Optional

from kiwii.data.datalayer import DataLayer
from kiwii.data.types import TDataStructure
from kiwii.shared.logging.componentloggername import ComponentLoggerName
from kiwii.shared.logging.logging import get_logger


class Data:
    """
    Dedicated class for persisting data layers to file. Used across the architecture elements to store data which needs
    to persist across reboots.
    """

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

        # if file does not already exist or is empty - write initial file
        if not self.filepath.is_file() or self.filepath.stat().st_size == 0:
            self._write(DataLayer())

    def store(self, data_structure: TDataStructure) -> None:
        """Stores provided data structure to storage"""

        # update data with new structure
        data_layer = self._read()
        data_layer.store(data_structure)

        # persist new data to file
        self._write(data_layer)

    def retrieve(self, data_structure_type: Type[TDataStructure]) -> Optional[TDataStructure]:
        """Returns requested data structure or `None` if one is not currently present in storage"""

        return self._read().retrieve(data_structure_type)

    def _write(self, data_layer: DataLayer) -> None:
        """Handles actual writing of `DataLayer` to disk."""

        with self.lock:
            with self.filepath.open("w") as _file:
                _file.write(data_layer.serialize())

    def _read(self) -> DataLayer:
        """Handles actual reading of `DataLayer` from disk."""

        with self.lock:
            with self.filepath.open("r") as _file:
                return DataLayer.deserialize(_file.read())
