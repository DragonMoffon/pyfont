from __future__ import annotations
from pathlib import Path

from .exceptions import MissingFontError, MissingTableError, ParseError
from .font import Font, Reader, TableRecord, Table
from .tables import TTCHeader
from .parsing import parse_tcc_header, parse_table_directory, parsers



# Collection Fonts have less control over their own bytes, and need to ask the Collection
# for some data, this should have no impact on the end user
class CollectionFont(Font):

    def __init__(self, offset: int, source: Collection) -> None:
        self._offset: int
        self._source: Collection = source

        table_directory = parse_table_directory(self, offset)
        self._records: dict[str, TableRecord] = {
            record.tableTag: record for record in table_directory.tableRecords
        }
        self._tables: dict[str, Table] = {"directory": table_directory}
    
    def validate_font(self) -> bool:
        return True # Font collections do not have the validation file fonts have.

    def get_record(self, name: str) -> TableRecord:
        if name not in self._records:
            raise MissingTableError(name)

        return self._records[name]

    def get_table_names(self) -> tuple[str, ...]:
        return tuple(self._records.keys())

    def get_tables(self) -> tuple[Table, ...]:
        return tuple(self._tables.values())

    def get_table(self, name: str) -> Table | None:
        if name in self._tables:
            return self._tables[name]

        if name not in self._records:
            raise MissingTableError(name)

        record = self._records[name]
        table = parsers[name](self, record)
        if table is None: # type: ignore -- undefined parsers return None
            raise ParseError(name)
        self._tables[record.tableTag] = table

        return table

    def has_table(self, name: str) -> bool:
        return name in self._records or name in self._tables

    def is_table_parsed(self, name: str) -> bool:
        return name in self._tables
    
    def seek(self, offset: int) -> None:
        self._source.seek(offset)

    def read(self, sz: int) -> bytes:
        return self._source.read(sz)

    def pointer(self) -> int:
        return self._source.pointer()


class Collection(Reader):
    
    def __init__(self, data: bytes, src: Path | None = None) -> None:
        self._data: bytes = data
        self._src: Path | None = src

        self._byte_offset: int = 0

        self._header = parse_tcc_header(self, 0)
        self._fonts: dict[int, CollectionFont] = {}

    @property
    def header(self) -> TTCHeader:
        return self._header
    
    def get_font(self, idx: int) -> CollectionFont:
        if idx in self._fonts:
            return self._fonts[idx]

        if self._header.numFonts <= idx:
            raise MissingFontError(idx)
        
        font = CollectionFont(self._header.tableDirectoryOffsets[idx], self)
        self._fonts[idx] = font
        return font
    
    def get_fonts(self) -> tuple[CollectionFont, ...]:
        for idx in range(self._header.numFonts):
            self.get_font(idx)
        return tuple(self._fonts.values())

    def has_font(self, idx: int):
        return 0 <= idx < self._header.numFonts

    def is_font_created(self, idx: int):
        return idx in self._fonts

    def seek(self, offset: int) -> None:
        self._byte_offset = offset

    def read(self, sz: int) -> bytes:
        n = self._byte_offset + sz
        d = self._data[self._byte_offset : n]
        self._byte_offset = n
        return d

    def pointer(self) -> int:
        return self._byte_offset
