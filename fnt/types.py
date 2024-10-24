from __future__ import annotations
from typing import Any, Self, Protocol
from types import new_class
from collections.abc import Callable
import dataclasses
import struct

__all__ = (
    "uint8",
    "int8",
    "uint16",
    "int16",
    "uint24",
    "int24",
    "uint32",
    "int32",
    "fixed",
    "FWORD",
    "UFWORD",
    "F2DOT14",
    "LONGDATETIME",
    "Tag",
    "Offset8",
    "Offset16",
    "Offset24",
    "Offset32",
    "Version16Dot16",
    "Table",
)


class _ttf_type:
    fmt: str = None  # Byte format for struct pack/unpack
    sz: int = None  # Byte size equal to struct.calcsize(cls)

    @classmethod
    def read(cls: Self, buffer: bytes, offset: int = 0) -> Self:
        if cls.sz is None:
            raise TypeError(f"{cls} is not a fully formed ttf type")

        b = buffer[offset : offset + cls.sz]
        if len(b) < cls.sz:
            raise ValueError(
                f"buffer {buffer} with offset {offset} is too small for {cls}"
            )

        return cls(b)


class uint8(int, _ttf_type):
    fmt: str = "c"
    sz: int = 1

    def __new__(cls: Self, b: bytes = b"\x00") -> Self:
        return int.__new__(cls, b[0])


class int8(int, _ttf_type):
    fmt: str = "c"
    sz: int = 1

    def __new__(cls: Self, b: bytes = b"\x00") -> Self:
        # Do 2-compliment if most significant bit is active
        return int.__new__(cls, b[0] - ((b[0] & 0x80) << 1))


class uint16(int, _ttf_type):
    fmt: str = "2c"
    sz: int = 2

    def __new__(cls: Self, b: bytes = b"\x00\x00") -> Self:
        return int.__new__(cls, (b[0] << 8) + b[1])


class int16(int, _ttf_type):
    fmt: str = "2c"
    sz: int = 2

    def __new__(cls: Self, b: bytes = b"\x00\x00") -> Self:
        # Do 2-compliment if most significant bit is active
        return int.__new__(cls, (b[0] << 8) + b[1] - ((b[0] & 0x80) << 9))


class uint24(int, _ttf_type):
    fmt: str = "3c"
    sz: int = 3

    def __new__(cls: Self, b: bytes = b"\x00\x00\x00") -> Self:
        return int.__new__(cls, (b[0] << 16) + (b[1] << 8) + b[2])


class int24(int, _ttf_type):
    fmt: str = "3c"
    sz: int = 3

    def __new__(cls: Self, b: bytes = b"\x00\x00\x00") -> Self:
        # Do 2-compliment if most significant bit is active
        return int.__new__(cls, uint24(b) - ((b[0] & 0x80) << 17))


class uint32(int, _ttf_type):
    fmt: str = "4c"
    sz: int = 4

    def __new__(cls: Self, b: bytes = b"\x00\x00\x00\x00") -> Self:
        return int.__new__(cls, (b[0] << 24) + (b[1] << 16) + (b[2] << 8) + b[3])


class int32(int, _ttf_type):
    fmt: str = "4c"
    sz: int = 4

    def __new__(cls: Self, b: bytes = b"\x00\x00\x00\x00") -> Self:
        # Do 2-compliment if most significant bit is active
        return int.__new__(
            cls,
            (b[0] << 24) + (b[1] << 16) + (b[2] << 8) + b[3] - ((b[0] & 0x80) << 25),
        )


# Signed 32-bit float with 16.16 fixed split
class fixed(float, _ttf_type):
    fmt: str = "4c"
    sz: int = 4

    def __new__(cls: Self, b: bytes = b"\x00\x00\x00\x00") -> Self:
        integer = int16(b[0:2])
        fraction = uint16(b[2:4])
        return float.__new__(cls, integer + fraction / 0x10000)


# Alias to int16 for font design units
class FWORD(int, _ttf_type):
    fmt: str = "2c"
    sz: int = 2

    def __new__(cls: Self, b: bytes = b"\x00\x00") -> Self:
        return int.__new__(cls, int16(b))


# Alias to uint16 for font design units
class UFWORD(int, _ttf_type):
    fmt: str = "2c"
    sz: int = 2

    def __new__(cls: Self, b: bytes = b"\x00\x00") -> Self:
        return int.__new__(cls, uint16(b))


# 16-bit signed fixed float with 2.14 bit split
class F2DOT14(float, _ttf_type):
    fmt: str = "2c"
    sz: int = 2

    def __new__(cls: Self, b: bytes = b"\x00\x00") -> Self:
        # The F2DOT14 format consists of a signed, 2’s complement integer
        # and an unsigned fraction. To compute the actual value,
        # take the integer and add the fraction.
        integer_bits = 0xC0 & b[0]
        match integer_bits:
            case 0x00:  # 0b00000000
                integer = 0
            case 0x40:  # 0b01000000
                integer = 1
            case 0x80:  # 0b10000000
                integer = -2
            case 0xC0:  # 0b11000000
                integer = -1
        fraction = (((b[0] << 8) + b[1]) & 0x3FFF) / 0x4000
        return float.__new__(cls, integer + fraction)


# 64-bit signed int for seconds since 12:00 midnight jan 1 1904
class LONGDATETIME(int, _ttf_type):
    fmt: str = "8c"
    sz: int = 8

    def __new__(cls: Self, b: bytes = b"\x00\x00\x00\x00\x00\x00\x00\x00") -> Self:
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


# Tag of 4 8-bit uints (ASCII char) for identification
class Tag(tuple[int, int, int, int], _ttf_type):
    fmt: str = "4c"
    sz: int = 4

    def __new__(cls: Self, b: bytes = b"\x00\x00") -> Self:
        return tuple.__new__(cls, (b[0], b[1], b[2], b[3]))


# 8-bit offset in table, NULL = 0x00
class Offset8(int, _ttf_type):
    fmt: str = "c"
    sz: int = 1

    def __new__(cls: Self, b: bytes = b"\x00") -> Self:
        return int.__new__(cls, b[0])


# 16-bit offset in table, NULL = 0x0000
class Offset16(int, _ttf_type):
    fmt: str = "2c"
    sz: int = 2

    def __new__(cls: Self, b: bytes = b"\x00\x00") -> Self:
        return int.__new__(cls, uint16(b))


# 24-bit offset in table, NULL = 0x000000
class Offset24(int, _ttf_type):
    fmt: str = "3c"
    sz: int = 3

    def __new__(cls: Self, b: bytes = b"\x00\x00\x00") -> Self:
        return int.__new__(cls, uint24(b))


# 32-bit offset in table, NULL = 0x00000000
class Offset32(int, _ttf_type):
    fmt: str = "4c"
    sz: int = 4

    def __new__(cls: Self, b: bytes = b"\x00\x00\x00\x00") -> Self:
        return int.__new__(cls, uint32(b))


# 2 16-bit uints (2nd uses only first 4 bits)
class Version16Dot16(tuple[int, int], _ttf_type):
    fmt: str = "4c"
    sz: int = 4

    def __new__(cls: Self, b: bytes = b"\x00\x00\x00\x00") -> Self:
        # The upper 16 bits comprise a major version number,
        # and the lower 16 bits, a minor version. Non-zero minor
        # version numbers are represented using digits 0 to 9 in
        # the highest-order nibbles of the lower 16 bits
        return tuple.__new__(cls, (b[0] << 8 + b[1], (b[2] & 0xF0) >> 4))


# An array of fixed type and length. Supports
class Array(tuple, _ttf_type):
    __typ__: type[_ttf_type] = None
    __ln__: int = 0

    def __new__(cls, b: bytes = b""):
        if cls.__typ__ is None:
            raise TypeError(f"{cls} is not a fully formed Array")

        offset = 0
        items = [None] * cls.__ln__
        for idx in range(cls.__ln__):
            items[idx] = item = cls.__typ__.read(b, offset)
            if item.sz is None or item.fmt is None:
                raise ValueError(
                    f"failed to create a fully formed ttf item of type {cls.__typ__} in {cls} from buffer {b} at offset {offset}"
                )
            offset += item.sz

        array = tuple.__new__(cls, items)
        array.fmt = "".join(item.fmt for item in array)
        array.sz = struct.calcsize(array.fmt)

        return array

    @classmethod
    def read(cls, buffer: bytes, offset: int = 0):
        if cls.__typ__ is None:
            raise TypeError(f"{cls} is not a fully formed Array")

        if cls.__typ__.sz is not None:
            b = buffer[offset : offset + cls.__ln__ * cls.__typ__.sz]
            if len(b) < cls.__ln__ * cls.__typ__.sz:
                raise ValueError(
                    f"buffer {buffer} with offset {offset} is too small for {cls}"
                )
            return cls(b)

        return cls(buffer[offset:])

    def __class_getitem__(
        cls: Self, inp: type[_ttf_type] | int | tuple[_ttf_type, int]
    ):
        if isinstance(inp, tuple):
            if len(inp) != 2:
                raise TypeError("{cls} only accepts up to two type arguments")
            typ, ln = inp

            if not isinstance(ln, int):
                raise TypeError(
                    "{cls} only accepts an integer length for the second argument"
                )
            if not isinstance(typ, type):
                raise TypeError("{cls} only accepts types for the first argument")

            newcls = new_class("Array", (cls,))
            newcls.__typ__ = typ
            newcls.__ln__ = ln
            return newcls
        elif isinstance(inp, type):
            newcls = new_class("Array", (cls,))
            newcls.__typ__ = inp
            return newcls
        elif cls.__typ__ is None:
            raise TypeError(f"{cls} is not a fully formed Array")
        elif not isinstance(inp, int):
            raise TypeError(
                f"{cls} only accepts an integer length when partially formed"
            )
        else:
            cls.__ln__ = inp
            return cls
        return cls

    def __str__(self) -> str:
        if self.__typ__ is None:
            return f"Invalid[]({','.join(str(item) for item in self)})"
        return f"{self.__typ__}[{self.__ln__}]({','.join(str(item) for item in self)})"

    def __repr__(self) -> str:
        return self.__str__()


# NOTE: Due to a limitation in dataclasses' field and fields methods all values found
# in the actual table, even if used soley for derivation (or padding) must be real
# fields in the final dataclass and cannot soley be an init arg


class DynamicFunction(Protocol):
    def __call__(self, *srcs, typ: type[_ttf_type], buffer: bytes, offset: int = 0): ...


# staticEntry - Found in the table as is (default)
# dynamicEntry - Real value must be calcuated, and does not have to be in table by default


def static():
    return dataclasses.field(metadata={"entry": "static"})


def dynamic(f: DynamicFunction, *srcs, derived: bool = False):
    return dataclasses.field(
        metadata={"entry": "dynamic", "derived": derived, "srcs": srcs, "func": f}
    )


def _parse_static(typ: type[_ttf_type], buffer: bytes, offset: int = 0):
    item = typ.read(buffer, offset)
    if item.sz is None or item.fmt is None:
        raise ValueError(f"Failed to create {typ} from buffer {buffer} at {offset}")
    return item


class Table(_ttf_type):
    __versions__: dict[_ttf_type, type[Table]] = None

    @classmethod
    def read(cls: Self, buffer: bytes, offset: int = 0) -> Self:
        # No versions were defined so use the default (initial definition)
        if not cls.__versions__:
            return cls._read(buffer, offset)

        version_field = dataclasses.fields(cls)[0]  # Assuming version is always first
        version_type: _ttf_type = version_field.type
        version = version_type.read(buffer, offset)
        print(version)
        return cls.__versions__.get(version, cls)._read(buffer, offset)

    @classmethod
    def read_version(cls: Self, v: _ttf_type, buffer: bytes, offset: int = 0) -> Self:
        if v not in cls.__versions__:
            raise ValueError(f"Version {v} was never defined for {cls}")
        return cls.__versions__[v]._read(buffer, offset)

    @classmethod
    def _read(cls: Self, buffer: bytes, offset: int) -> Self:
        # Many table formats have variable length arrays that make
        # using struct.unpack difficult, but each type still has it fmt.
        fields = dataclasses.fields(cls)
        values: dict[str, _ttf_type] = {}
        fmt = ""  # Table's final struct fmt
        sz = 0  # Table's final byte size, Also used as the rolling offset
        for field in fields:
            typ = field.type  # Metamagic of dataclasses.Field stores the type
            name = field.name  # Name of the Field from the dataclass def
            entry = field.metadata.get("entry", "static")
            if entry == "static":  # This entry can be read as-is from the buffer
                item = _parse_static(typ, buffer, offset + sz)
                values[name] = item
                sz += item.sz
                fmt += item.fmt
            elif entry == "dynamic":
                # This entry has to be modified/derived instead of the raw value
                derived = field.metadata.get("derived", False)
                srcs = field.metadata.get("srcs", ())
                func = field.metadata.get("func", _parse_static)

                item = func(*(values[src] for src in srcs), typ, buffer, offset + sz)
                values[name] = item
                if not derived:
                    # If the entry was actually found in the table then we need to
                    # offset the buffer, and add it to the format string.
                    sz += item.sz
                    fmt += item.fmt
            else:
                raise TypeError(
                    f'Table entry type {entry} is not supported, use "static" or "dynamic"'
                )

        obj = cls(*values.values())
        obj.fmt = fmt
        obj.sz = sz

        return obj

    @classmethod
    def version(cls: Self, v: _ttf_type) -> Self:
        if not isinstance(v, _ttf_type):
            raise ValueError(f"{v} is not a ttf type and cannot be used for versioning")

        def wrap(subcls: type[Self]):
            cls.__versions__[v] = dataclasses.dataclass(subcls)
            return cls

        return wrap


def definition(cls: type[Table]) -> type[Table]:
    cls = dataclasses.dataclass(cls)
    cls.__versions__ = {}
    return cls
