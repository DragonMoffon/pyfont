from typing import TypeVar, Generic
from dataclasses import dataclass

__all__ = (
    "uint8",
    "uint8_from_bytes",
    "uint8_to_bytes",
    "int8",
    "int8_from_bytes",
    "int8_to_bytes",
    "uint16",
    "uint16_from_bytes",
    "uint16_to_bytes",
    "int16",
    "int16_from_bytes",
    "int16_to_bytes",
    "uint24",
    "uint24_from_bytes",
    "uint24_to_bytes",
    "int24",
    "int24_from_bytes",
    "int24_to_bytes",
    "uint32",
    "uint32_from_bytes",
    "uint32_to_bytes",
    "int32",
    "int32_from_bytes",
    "int32_to_bytes",
    "fixed",
    "fixed_from_bytes",
    "fixed_to_bytes",
    "UFWORD",
    "UFWORD_from_bytes",
    "UFWORD_to_bytes",
    "FWORD",
    "FWORD_from_bytes",
    "FWORD_to_bytes",
    "F2DOT14",
    "F2DOT14_from_bytes",
    "F2DOT14_to_bytes",
    "LONGDATETIME",
    "LONGDATETIME_from_bytes",
    "LONGDATETIME_to_bytes",
    "tag",
    "tag_from_bytes",
    "tag_to_bytes",
    "offset8",
    "offset8_from_bytes",
    "offset8_to_bytes",
    "offset16",
    "offset16_from_bytes",
    "offset16_to_bytes",
    "offset24",
    "offset24_from_bytes",
    "offset24_to_bytes",
    "offset32",
    "offset32_from_bytes",
    "offset32_to_bytes",
    "version16dot16",
    "version16dot16_from_bytes",
    "version16dot16_to_bytes",
    "table",
)

# types
type uint8 = int
type int8 = int
type uint16 = int
type int16 = int
type uint24 = int
type int24 = int
type uint32 = int
type int32 = int
type fixed = float
type UFWORD = int
type FWORD = int
type F2DOT14 = float
type LONGDATETIME = int
type tag = str
type offset8 = int
type offset16 = int
type offset24 = int
type offset32 = int
type version16dot16 = tuple[int, int]


# Unsigned Integers
def uint8_from_bytes(b: bytes) -> uint8:
    return int.from_bytes(b[:1], signed=False)


def uint8_to_bytes(v: uint8) -> bytes:
    return v.to_bytes(1, signed=False)


def uint16_from_bytes(b: bytes) -> uint16:
    return int.from_bytes(b[:2], signed=False)


def uint16_to_bytes(v: uint16) -> bytes:
    return v.to_bytes(2, signed=False)


def uint24_from_bytes(b: bytes) -> uint24:
    return int.from_bytes(b[:3], signed=False)


def uint24_to_bytes(v: uint24) -> bytes:
    return v.to_bytes(3, signed=False)


def uint32_from_bytes(b: bytes) -> uint32:
    return int.from_bytes(b[:4], signed=False)


def uint32_to_bytes(v: uint32) -> bytes:
    return v.to_bytes(4, signed=False)


# Signed Integers
def int8_from_bytes(b: bytes) -> int8:
    return int.from_bytes(b[:1], signed=True)


def int8_to_bytes(v: int8) -> bytes:
    return v.to_bytes(1, signed=True)


def int16_from_bytes(b: bytes) -> int16:
    return int.from_bytes(b[:2], signed=True)


def int16_to_bytes(v: int16) -> bytes:
    return v.to_bytes(2, signed=True)


def int24_from_bytes(b: bytes) -> int24:
    return int.from_bytes(b[:3], signed=True)


def int24_to_bytes(v: int24) -> bytes:
    return v.to_bytes(3, signed=True)


def int32_from_bytes(b: bytes) -> int32:
    return int.from_bytes(b[:4], signed=True)


def int32_to_bytes(v: int32) -> bytes:
    return v.to_bytes(4, signed=True)


# Offsets
def offset8_from_bytes(b: bytes) -> offset8:
    return uint8_from_bytes(b)


def offset8_to_bytes(v: offset8) -> bytes:
    return uint8_to_bytes(v)


def offset16_from_bytes(b: bytes) -> offset16:
    return uint16_from_bytes(b)


def offset16_to_bytes(v: offset16) -> bytes:
    return uint16_to_bytes(v)


def offset24_from_bytes(b: bytes) -> offset24:
    return uint24_from_bytes(b)


def offset24_to_bytes(v: offset24) -> bytes:
    return uint16_to_bytes(v)


def offset32_from_bytes(b: bytes) -> offset32:
    return uint32_from_bytes(b)


def offset32_to_bytes(v: offset32) -> bytes:
    return uint32_to_bytes(v)


# Decimal Values
def fixed_from_bytes(b: bytes) -> fixed:
    return int32_from_bytes(b) / (1 << 16)


def fixed_to_bytes(v: fixed) -> bytes:
    return int32_to_bytes(int(v * (1 << 16)))


def F2DOT14_from_bytes(b: bytes) -> F2DOT14:
    return int16_from_bytes(b) / (1 << 14)


def F2DOT14_to_bytes(v: F2DOT14) -> bytes:
    return int16_to_bytes(int(v * (1 << 14)))


# Words


def UFWORD_from_bytes(b: bytes) -> UFWORD:
    return uint16_from_bytes(b)


def UFWORD_to_bytes(v: UFWORD) -> bytes:
    return uint16_to_bytes(v)


def FWORD_from_bytes(b: bytes) -> FWORD:
    return int16_from_bytes(b)


def FWORD_to_bytes(v: FWORD) -> bytes:
    return int16_to_bytes(v)


# Other


def LONGDATETIME_from_bytes(b: bytes) -> LONGDATETIME:
    return int.from_bytes(b[:9], signed=True)


def LONGDATETIME_to_bytes(v: LONGDATETIME) -> bytes:
    return v.to_bytes(8, signed=True)


def tag_from_bytes(b: bytes) -> tag:
    return f"{chr(b[0])}{chr(b[1])}{chr(b[2])}{chr(b[3])}"


def tag_to_bytes(v: tag) -> bytes:
    return (
        uint8_to_bytes(ord(v[0]))
        + uint8_to_bytes(ord(v[1]))
        + uint8_to_bytes(ord(v[2]))
        + uint8_to_bytes(ord(v[3]))
    )


def version16dot16_from_bytes(b: bytes) -> version16dot16:
    return uint16_from_bytes(b[:2]), (b[2] & 0xF0) >> 4


def version16dot16_to_bytes(v: version16dot16) -> bytes:
    return uint16_to_bytes(v[0]) + uint16_to_bytes(v[1] << 12)


table = dataclass
