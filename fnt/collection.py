from pathlib import Path

from .exceptions import MissingTableError
from .types import uint32
from .font import Font, Reader, TableRecord, Table
from .tables import TTCHeader
from .parsing import parse_tcc_header



# Collection Fonts have less control over their own bytes, and need to ask the Collection
# for some data, this should have no impact on the end user
class CollectionFont(Font):
    
    def validate_font(self) -> bool:
        raise NotImplementedError()

    def get_record(self, name: str) -> TableRecord:
        raise NotImplementedError()

    def compute_checksum(self, start: int, length: int) -> uint32:
        raise NotImplementedError()

    def compute_table_checksum(self, name: str) -> uint32:
        raise NotImplementedError()

    def validate_checksum(self, name: str) -> bool:
        if not self.has_table(name):
            raise MissingTableError(name)
        record = self.get_record(name)
        checksum = self.compute_table_checksum(name)
        
        return checksum == record.checksum

    def get_table_names(self) -> tuple[str, ...]:
        raise NotImplementedError()

    def get_tables(self) -> tuple[Table, ...]:
        raise NotImplementedError()

    def get_table(self, name: str) -> Table | None:
        raise NotImplementedError()

    def has_table(self, name: str) -> bool:
        raise NotImplementedError()

    def is_table_parsed(self, name: str) -> bool:
        raise NotImplementedError()
    
    def seek(self, offset: int) -> None:
        raise NotImplementedError()

    def read(self, sz: int) -> bytes:
        raise NotImplementedError()

    def pointer(self) -> int:
        raise NotImplementedError()



class Collection(Reader):
    
    def __init__(self, data: bytes, src: Path | None = None) -> None:
        self._data: bytes = data
        self._src: Path | None = src

        self._byte_offset: int = 0

        self._header = parse_tcc_header(self, 0)

    @property
    def header(self) -> TTCHeader:
        return self._header

    def seek(self, offset: int) -> None:
        self._byte_offset = offset

    def read(self, sz: int) -> bytes:
        n = self._byte_offset + sz
        d = self._data[self._byte_offset : n]
        self._byte_offset = n
        return d

    def pointer(self) -> int:
        return self._byte_offset
