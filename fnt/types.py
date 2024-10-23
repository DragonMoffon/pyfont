from __future__ import annotations
from typing import Any, Self
import dataclasses
import struct

__all__ = (
    "uint8",
    "uint8_s",
    "uint8_t",
    "int8",
    "int8_s",
    "int8_t",
    "uint16",
    "uint16_s",
    "uint16_t",
    "int16",
    "int16_s",
    "int16_t",
    "uint24",
    "uint24_s",
    "uint24_t",
    "int24",
    "int24_s",
    "int24_t",
    "uint32",
    "uint32_s",
    "uint32_t",
    "int32",
    "int32_s",
    "int32_t",
    "fixed",
    "fixed_s",
    "fixed_t",
    "FWORD",
    "FWORD_s",
    "FWORD_t",
    "UFWORD",
    "UFWORD_s",
    "UFWORD_t",
    "F2DOT14",
    "F2DOT14_s",
    "F2DOT14_t",
    "LONGDATETIME",
    "LONGDATETIME_s",
    "LONGDATETIME_t",
    "Tag",
    "Tag_s",
    "Tag_t",
    "Offset8",
    "Offset8_s",
    "Offset8_t",
    "Offset16",
    "Offset16_s",
    "Offset16_t",
    "Offset24",
    "Offset24_s",
    "Offset24_t",
    "Offset32",
    "Offset32_s",
    "Offset32_t",
    "Version16Dot16",
    "Version16Dot16_s",
    "Version16Dot16_t",
    "Table",
)


# -- Struct Aliases --
uint8_s = "c"  # Unsigned 8-bit int
int8_s = "c"  # Signed 8-bit int
uint16_s = "2c"  # Unsigned 16-bit int
int16_s = "2c"  # Signed 16-bit int
uint24_s = "3c"  # Unsigned 24-bit int
int24_s = "3c"  # Signed 24-bit int
uint32_s = "4c"  # Unsigned 32-bit int
int32_s = "4c"  # Signed 32-bit int
fixed_s = "4c"  # Signed 32-bit float with 16.16 fixed split
FWORD_s = "2c"  # Alias to int16 for font design units
UFWORD_s = "2c"  # Alias to uint16 for font design units
F2DOT14_s = "2c"  # 16-bit signed fixed float with 2.14 bit split
LONGDATETIME_s = "8c"  # 64-bit signed int for seconds since 12:00 midnight jan 1 1904
Tag_s = "4c"  # Tag of 4 8-bit uints for identification
Offset8_s = "c"  # 8-bit offset in table, NULL = 0b00
Offset16_s = "2c"  # 16-bit offset in table, NULL = 0b0000
Offset24_s = "3c"  # 24-bit offset in table, NULL = 0b000000
Offset32_s = "4c"  # 32-bit offset in table, NULL = 0b00000000
Version16Dot16_s = "4c"  # 2 16-bit bytes (2nd is little endian)


type uint8_t = int
type int8_t = int
type uint16_t = int
type int16_t = int
type uint24_t = int
type int24_t = int
type uint32_t = int
type int32_t = int
type fixed_t = float
type FWORD_t = int
type UFWORD_t = int
type F2DOT14_t = float
type LONGDATETIME_t = int
type Tag_t = tuple[int, int, int, int]
type Offset8_t = int
type Offset16_t = int
type Offset24_t = int
type Offset32_t = int
type Version16Dot16_t = tuple[int, int]


def uint8(b: bytes) -> uint8_t:
    return b[0]


def int8(b: bytes) -> int8_t:
    # Do 2-compliment if most significant bit is active
    return uint8(b) - ((b[0] & 0x80) << 1)


def uint16(b: bytes) -> uint16_t:
    return (b[0] << 8) + b[1]


def int16(b: bytes) -> int16_t:
    # Do 2-compliment if most significant bit is active
    return uint16(b) - ((b[0] & 0x80) << 9)


def uint24(b: bytes) -> int24_t:
    return (b[0] << 16) + (b[1] << 8) + b[2]


def int24(b: bytes) -> int24_t:
    # Do 2-compliment if most significant bit is active
    return uint24(b) - ((b[0] & 0x80) << 17)


def uint32(b: bytes) -> int32_t:
    return (b[0] << 24) + (b[1] << 16) + (b[2] << 8) + b[3]


def int32(b: bytes) -> int32_t:
    # Do 2-compliment if most significant bit is active
    return uint32(b) - ((b[0] & 0x80) << 25)


def fixed(b: bytes) -> fixed_t:
    integer = int16(b[0:2])
    fraction = uint16(b[2:4])
    return integer + fraction / 0x10000


def FWORD(b: bytes) -> FWORD_t:
    return int16(b)


def UFWORD(b: bytes) -> UFWORD_t:
    return uint16(b)


def F2DOT14(b: bytes) -> F2DOT14_t:
    # The F2DOT14 format consists of a signed, 2’s complement integer
    # and an unsigned fraction. To compute the actual value,
    # take the integer and add the fraction.
    integer_bits = 0xC0 & b[0]
    match integer_bits:
        case 0x00:
            integer = 0
        case 0x40:
            integer = 1
        case 0x80:
            integer = -2
        case 0xC0:
            integer = -1
    fraction = (((b[0] << 8) + b[1]) & 0x3FFF) / 0x4000
    return integer + fraction


def LONGDATETIME(b: bytes) -> LONGDATETIME_t:
    return (
        (b[0] << 56)
        + (b[1] << 48)
        + (b[2] << 40)
        + (b[3] << 32)
        + (b[4] << 24)
        + (b[5] << 16)
        + (b[6] << 8)
        + b[7]
    )


def Tag(b: bytes) -> Tag_t:
    return b[0], b[1], b[2], b[3]


def Offset8(b: bytes) -> Offset8_t:
    return uint8(b)


def Offset16(b: bytes) -> Offset16_t:
    return uint16(b)


def Offset24(b: bytes) -> Offset24_t:
    return uint24(b)


def Offset32(b: bytes) -> Offset32_t:
    return uint32(b)


def Version16Dot16(b: bytes) -> Version16Dot16_t:
    # The upper 16 bits comprise a major version number,
    # and the lower 16 bits, a minor version. Non-zero minor
    # version numbers are represented using digits 0 to 9 in
    # the highest-order nibbles of the lower 16 bits
    return (b[0] << 8) + b[1], (b[2] & 0xF0) >> 4


_construct: dict[str, callable[[bytes], Any]] = {
    "uint8_t": uint8,
    "int8_t": int8,
    "uint16_t": uint16,
    "int16_t": int16,
    "uint24_t": uint24,
    "int24_t": int24,
    "uint32_t": uint32,
    "int32_t": int32,
    "fixed_t": fixed,
    "FWORD_t": FWORD,
    "UFWORD_t": UFWORD,
    "F2DOT14_t": F2DOT14,
    "LONGDATETIME_t": LONGDATETIME,
    "Tag_t": Tag,
    "Offset8_t": Offset8,
    "Offset16_t": Offset16,
    "Offset24_t": Offset24,
    "Offset32_t": Offset32,
    "Version16Dot16_t": Version16Dot16,
}

_struct: dict[str, str] = {
    "uint8_t": uint8_s,
    "int8_t": int8_s,
    "uint16_t": uint16_s,
    "int16_t": int16_s,
    "uint24_t": uint24_s,
    "int24_t": int24_s,
    "uint32_t": uint32_s,
    "int32_t": int32_s,
    "fixed_t": fixed_s,
    "FWORD_t": FWORD_s,
    "UFWORD_t": UFWORD_s,
    "F2DOT14_t": F2DOT14_s,
    "LONGDATETIME_t": LONGDATETIME_s,
    "Tag_t": Tag_s,
    "Offset8_t": Offset8_s,
    "Offset16_t": Offset16_s,
    "Offset24_t": Offset24_s,
    "Offset32_t": Offset32_s,
    "Version16Dot16_t": Version16Dot16_s,
}


@dataclasses.dataclass
class Table:
    @classmethod
    def fmt(cls: Self) -> str:
        return "!" + "".join(_struct[f] for f in cls.fields())

    @classmethod
    def size(cls: Self) -> int:
        return struct.calcsize(cls.fmt())

    @classmethod
    def get(cls: Self, buffer, offset: int = 0) -> Self:
        fields = cls.fields()
        fmt = "!" + "".join(_struct[f] for f in fields)
        data = struct.unpack_from(fmt, buffer=buffer, offset=offset)
        return cls(*(_construct[f](d) for f, d in zip(fields, data)))

    @classmethod
    def fields(cls: Self) -> tuple[str, ...]:
        return tuple(f.type.__name__ for f in dataclasses.fields(cls))
