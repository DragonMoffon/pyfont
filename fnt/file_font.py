from pathlib import Path

from .font import Font
from .tables import Table, TableRecord
from .parsing import parsers, parse_table_directory


# File Fonts hold and manage their own byte data. They can do what the like with it, and
# aren't beholdent to a collection.
class FileFont(Font):
    def __init__(self, data: bytes, src: Path | None = None):
        self._data: bytes = data
        self._src = src

        self._byte_offset: int = 0

        table_directory = parse_table_directory(self, 0)
        self._records: dict[str, TableRecord] = {
            record.tableTag: record for record in table_directory.tableRecords
        }
        self._tables: dict[str, Table] = {"TableDirectory": table_directory}

    def seek(self, offset: int):
        self._byte_offset = offset

    def read(self, sz: int) -> bytes:
        n = self._byte_offset + sz
        b = self._data[self._byte_offset : n]
        self._byte_offset = n
        return b

    def get_record(self, name: str) -> TableRecord:
        if name not in self._records:
            # TODO: make custom error for this
            raise KeyError(f"font does not contain the table [{name}]")

        return self._records[name]

    def get_table_names(self) -> tuple[str, ...]:
        return tuple(self._records.keys())

    def get_tables(self) -> tuple[Table, ...]:
        return tuple(self._tables.values())

    def get_table(self, name: str) -> Table | None:
        if name in self._tables:
            return self._tables[name]

        if name not in self._records:
            raise KeyError(f"font does not contain the table [{name}]")

        record = self._records[name]
        table = parsers[name](self, record)
        self._tables[record.tableTag] = table

        return table

    def has_table(self, name: str) -> bool:
        return name in self._records

    def is_table_parsed(self, name: str) -> bool:
        return name in self._tables

    @classmethod
    def from_file(cls, file: Path):
        with open(file, "rb") as fp:
            data = fp.read()
        return cls(data, file)
