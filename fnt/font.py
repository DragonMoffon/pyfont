from pathlib import Path

from .tables import TABLES, Table, tableDirectory, TableRecord


# Abstract
class Font:
    def get_tables(self) -> tuple[str, ...]: ...

    def get_table(self, name: str) -> Table | None: ...

    def has_table(self, name: str) -> bool: ...

    def is_table_parsed(self, name: str) -> bool: ...


# File Fonts hold and manage their own byte data. They can do what the like with it, and
# aren't beholdent to a collection.
class FileFont(Font):

    def __init__(self, data: bytes, src: Path | None = None):
        self._data = data
        self._src = src

        self._tables: dict[str, Table] = {}
        self._name_mapping: dict[str, TableRecord] = {}

        root = tableDirectory.read(data)
        for record in root.tableRecords:
            self._name_mapping[str(record.tableTag)] = record
        self._tables["tableDirectory"] = root

    def get_tables(self) -> tuple[str, ...]:
        union = set((*self._name_mapping.keys(), *self._tables.keys()))
        return tuple(sorted(union))

    def get_table[TableType: Table](self, name: str) -> TableType | None:
        if name not in TABLES:
            print(f"{name} is not a valid TTF or OTF table")
            return None

        if name in self._tables:
            return self._tables[name]

        if name not in self._name_mapping:
            print(f"{name} is not found within Font")
            return None

        record = self._name_mapping[name]
        typ: type[TableType] = TABLES[name]

        table = typ.read(self._data, record.offset, font=self)

        return table

    def has_table(self, name: str) -> bool:
        return name in self._name_mapping

    def is_table_parsed(self, name: str) -> bool:
        return name in self._tables

    @classmethod
    def from_file(cls, file: Path):
        with open(file, "rb") as fp:
            data = fp.read()
        return cls(data, file)


# Collection Fonts have less control over their own bytes, and need to ask the Collection
# for some data, this should have no impact on the end user
class CollectionFont(Font):
    pass
