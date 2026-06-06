from typing import Callable

from .tables import Table, TableRecord
from .exceptions import MissingTableError
from .types import (
    uint8,
    int8,
    uint16,
    int16,
    uint24,
    int24,
    uint32,
    int32,
    fixed,
    F2DOT14,
    LONGDATETIME,
    tag,
    version16dot16,
    uint8_from_bytes,
    int8_from_bytes,
    uint16_from_bytes,
    int16_from_bytes,
    uint24_from_bytes,
    int24_from_bytes,
    uint32_from_bytes,
    int32_from_bytes,
    fixed_from_bytes,
    F2DOT14_from_bytes,
    LONGDATETIME_from_bytes,
    tag_from_bytes,
    version16dot16_from_bytes,
)

__all__ = ("Font", "ParseMethod", "TableRef")


# Abstract
class Reader:
    def seek(self, offset: int) -> None:
        raise NotImplementedError()

    def read(self, sz: int) -> bytes:
        raise NotImplementedError()

    def pointer(self) -> int:
        raise NotImplementedError()

    def get_uint8(self) -> uint8:
        return uint8_from_bytes(self.read(1))

    def get_int8(self) -> int8:
        return int8_from_bytes(self.read(1))

    def get_uint16(self) -> uint16:
        return uint16_from_bytes(self.read(2))

    def get_int16(self) -> int16:
        return int16_from_bytes(self.read(2))

    def get_uint24(self) -> uint24:
        return uint24_from_bytes(self.read(3))

    def get_int24(self) -> int24:
        return int24_from_bytes(self.read(3))

    def get_uint32(self) -> uint32:
        return uint32_from_bytes(self.read(4))

    def get_int32(self) -> int32:
        return int32_from_bytes(self.read(4))

    def get_fixed(self) -> fixed:
        return fixed_from_bytes(self.read(4))

    def get_F2DOT14(self) -> F2DOT14:
        return F2DOT14_from_bytes(self.read(2))

    def get_time(self) -> LONGDATETIME:
        return LONGDATETIME_from_bytes(self.read(8))

    def get_tag(self) -> tag:
        return tag_from_bytes(self.read(4))

    def get_version_legacy(self) -> version16dot16:
        return version16dot16_from_bytes(self.read(4))

    get_offset8 = get_uint8
    get_offset16 = get_uint16
    get_offset32 = get_uint32
    get_UFWORD = get_uint16
    get_FWORD = get_int16

    def get_uint8_array(self, count: int) -> tuple[uint8, ...]:
        b = self.read(count)
        return tuple(uint8_from_bytes(b[i : i + 1]) for i in range(count))

    def get_int8_array(self, count: int) -> tuple[int8, ...]:
        b = self.read(count)
        return tuple(int8_from_bytes(b[i : i + 1]) for i in range(count))

    def get_uint16_array(self, count: int) -> tuple[uint16, ...]:
        b = self.read(2 * count)
        return tuple(uint16_from_bytes(b[2 * i : 2 * i + 2]) for i in range(count))

    def get_int16_array(self, count: int) -> tuple[int16, ...]:
        b = self.read(2 * count)
        return tuple(uint16_from_bytes(b[2 * i : 2 * i + 2]) for i in range(count))

    def get_uint24_array(self, count: int) -> tuple[uint24, ...]:
        b = self.read(3 * count)
        return tuple(uint24_from_bytes(b[3 * i : 3 * i + 3]) for i in range(count))

    def get_int24_array(self, count: int) -> tuple[int24, ...]:
        b = self.read(3 * count)
        return tuple(int24_from_bytes(b[3 * i : 3 * i + 3]) for i in range(count))

    def get_uint32_array(self, count: int) -> tuple[uint32, ...]:
        b = self.read(4 * count)
        return tuple(uint32_from_bytes(b[4 * i : 4 * i + 4]) for i in range(count))

    def get_int32_array(self, count: int) -> tuple[int32, ...]:
        b = self.read(4 * count)
        return tuple(int32_from_bytes(b[4 * i : 4 * i + 4]) for i in range(count))

    def get_fixed_array(self, count: int) -> tuple[fixed, ...]:
        b = self.read(4 * count)
        return tuple(fixed_from_bytes(b[4 * i : 4 * i + 4]) for i in range(count))

    def get_F2DOT14_array(self, count: int) -> tuple[F2DOT14, ...]:
        b = self.read(2 * count)
        return tuple(F2DOT14_from_bytes(b[2 * i : 2 * i + 2]) for i in range(count))

    def get_time_array(self, count: int) -> tuple[LONGDATETIME, ...]:
        b = self.read(8 * count)
        return tuple(LONGDATETIME_from_bytes(b[8 * i : 8 * i + 8]) for i in range(count))

    def get_tag_array(self, count: int) -> tuple[tag, ...]:
        b = self.read(4 * count)
        return tuple(tag_from_bytes(b[4 * i : 4 * i + 4]) for i in range(count))

    def get_version_legacy_array(self, count: int) -> tuple[version16dot16, ...]:
        b = self.read(4 * count)
        return tuple(version16dot16_from_bytes(b[4 * i : 4 * i + 4]) for i in range(count))

    get_offset8_array = get_uint8_array
    get_offset16_array = get_uint16_array
    get_offset24_array = get_uint24_array
    get_offset32_array = get_uint32_array
    get_UFWORD_array = get_uint16_array
    get_FWORD_array = get_int16_array


# Abstract
class Font(Reader):
    def validate_font(self) -> bool:
        raise NotImplementedError()

    def get_record(self, name: str) -> TableRecord:
        raise NotImplementedError()

    def compute_checksum(self, start: int, length: int) -> uint32:
        """
        Calculate the checksum for a range of bytes based on the OTF spec.
        This is a 32-bit unsigned integer so it has to be moduloed.

        To find the checksum interpret all of the bytes of the table as
        an array of 32-bit unsigned integers and sum them.

        The length of a table given by its record does not include any
        padding but the checksum (and the OTF spec) requires tables to
        be aligned to 4 bytes. The padding is assumed to be all zeros,
        but this is not checked.

        The head table requires special conciderations not taken in this function.
        """

        self.seek(start)
        # uses smart bit manipulation to ensure required padding is added.
        count = ((length + 3) & ~3) // 4
        return sum(self.get_uint32_array(count)) % 0x100000000

    def compute_table_checksum(self, name: str) -> uint32:
        if not self.has_table(name):
            raise MissingTableError(name)

        rec = self.get_record(name)
        if name != "head":
            return self.compute_checksum(rec.offset, rec.length)

        checksumAdjustmentOffset = rec.offset + 12
        before_adjustment = self.compute_checksum(rec.offset, 8)
        after_adjustment = self.compute_checksum(checksumAdjustmentOffset, rec.length - 12)

        return (before_adjustment + after_adjustment) % 0x100000000

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


type ParseMethod = Callable[[Font, TableRecord], Table]


# Table Property
class TableRef[T: Table]:
    # Generic override of table name for tables like OS/2
    def __init__(self, typ: type[T], name: str = ""):
        self._typ: type[T] = typ
        self._name: str = name or typ.__name__

    def __get__(self, obj: Font | None, objtype: None) -> T | None:
        if obj is None or not obj.has_table(self._name):
            return None
        return obj.get_table(self._name)  # type: ignore

    def __set__(self, obj: Font | None, value: None):
        raise TypeError("cannot set the value of a font table.")


class RequiredTableRef[T: Table]:
    # Generic override of table name for names like OS/2
    def __init__(self, typ: type[T], name: str = "") -> None:
        self._typ: type[T] = typ
        self._name: str = name or typ.__name__

    def __get__(self, obj: Font | None, objtype: None) -> T:
        if obj is None:
            return None  # type: ignore
        return obj.get_table(self._name)  # type: ignore
