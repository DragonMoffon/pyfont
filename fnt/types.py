from __future__ import annotations
from typing import Self, Protocol
import dataclasses

__all__ = (
    "TTFType",
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
    "Array",
    "static",
    "dynamic",
    "array",
    "definition",
    "Table",
)


class TTFType:
    fmt: str = None  # Byte format for struct pack/unpack
    sz: int = None  # Byte size equal to struct.calcsize(cls)

    @classmethod
    def read(cls: Self, buffer: bytes, offset: int = 0) -> Self:
        """
        Return the TTF type extracted from the bytes at the offset in the buffer.
        By default this is bounded by the type's size, but the Table and Array
        TTF type don't follow this convention and aren't bounded from above.
        This means that they won't immediatly throw a ValueError.
        """
        if cls.sz is None:
            raise TypeError(f"{cls} is not a fully formed ttf type")

        b = buffer[offset : offset + cls.sz]
        if len(b) < cls.sz:
            raise ValueError(
                f"buffer {buffer} with offset {offset} is too small for {cls}"
            )

        return cls(b)

    @classmethod
    def byte(cls: Self, val, signed: bool = False) -> Self:
        # byte is NOT a safe method of getting TTFType's but neccisary for
        # simple lambda functions.
        if cls.sz is None:
            raise ValueError("Cannot byte {cls} as it is not fully formed")
        return cls(val.to_bytes(length=cls.sz, signed=signed))


class TTFEnum:
    pass


class uint8(int, TTFType):
    fmt: str = "c"
    sz: int = 1

    def __new__(cls: Self, b: bytes = b"\x00") -> Self:
        return int.__new__(cls, b[0])


class int8(int, TTFType):
    fmt: str = "c"
    sz: int = 1

    def __new__(cls: Self, b: bytes = b"\x00") -> Self:
        # Do 2-compliment if most significant bit is active
        return int.__new__(cls, b[0] - ((b[0] & 0x80) << 1))


class uint16(int, TTFType):
    fmt: str = "2c"
    sz: int = 2

    def __new__(cls: Self, b: bytes = b"\x00\x00") -> Self:
        return int.__new__(cls, (b[0] << 8) + b[1])


class int16(int, TTFType):
    fmt: str = "2c"
    sz: int = 2

    def __new__(cls: Self, b: bytes = b"\x00\x00") -> Self:
        # Do 2-compliment if most significant bit is active
        return int.__new__(cls, (b[0] << 8) + b[1] - ((b[0] & 0x80) << 9))


class uint24(int, TTFType):
    fmt: str = "3c"
    sz: int = 3

    def __new__(cls: Self, b: bytes = b"\x00\x00\x00") -> Self:
        return int.__new__(cls, (b[0] << 16) + (b[1] << 8) + b[2])


class int24(int, TTFType):
    fmt: str = "3c"
    sz: int = 3

    def __new__(cls: Self, b: bytes = b"\x00\x00\x00") -> Self:
        # Do 2-compliment if most significant bit is active
        return int.__new__(cls, uint24(b) - ((b[0] & 0x80) << 17))


class uint32(int, TTFType):
    fmt: str = "4c"
    sz: int = 4

    def __new__(cls: Self, b: bytes = b"\x00\x00\x00\x00") -> Self:
        return int.__new__(cls, (b[0] << 24) + (b[1] << 16) + (b[2] << 8) + b[3])


class int32(int, TTFType):
    fmt: str = "4c"
    sz: int = 4

    def __new__(cls: Self, b: bytes = b"\x00\x00\x00\x00") -> Self:
        # Do 2-compliment if most significant bit is active
        return int.__new__(
            cls,
            (b[0] << 24) + (b[1] << 16) + (b[2] << 8) + b[3] - ((b[0] & 0x80) << 25),
        )


# Signed 32-bit float with 16.16 fixed split
class fixed(float, TTFType):
    fmt: str = "4c"
    sz: int = 4

    def __new__(cls: Self, b: bytes = b"\x00\x00\x00\x00") -> Self:
        integer = int16(b[0:2])
        fraction = uint16(b[2:4])
        return float.__new__(cls, integer + fraction / 0x10000)


# Alias to int16 for font design units
class FWORD(int, TTFType):
    fmt: str = "2c"
    sz: int = 2

    def __new__(cls: Self, b: bytes = b"\x00\x00") -> Self:
        return int.__new__(cls, int16(b))


# Alias to uint16 for font design units
class UFWORD(int, TTFType):
    fmt: str = "2c"
    sz: int = 2

    def __new__(cls: Self, b: bytes = b"\x00\x00") -> Self:
        return int.__new__(cls, uint16(b))


# 16-bit signed fixed float with 2.14 bit split
class F2DOT14(float, TTFType):
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
class LONGDATETIME(int, TTFType):
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
class Tag(tuple[int, int, int, int], TTFType):
    fmt: str = "4c"
    sz: int = 4

    def __new__(cls: Self, b: bytes = b"\x00\x00") -> Self:
        return tuple.__new__(cls, (b[0], b[1], b[2], b[3]))


# 8-bit offset in table, NULL = 0x00
class Offset8(int, TTFType):
    fmt: str = "c"
    sz: int = 1

    def __new__(cls: Self, b: bytes = b"\x00") -> Self:
        return int.__new__(cls, b[0])


# 16-bit offset in table, NULL = 0x0000
class Offset16(int, TTFType):
    fmt: str = "2c"
    sz: int = 2

    def __new__(cls: Self, b: bytes = b"\x00\x00") -> Self:
        return int.__new__(cls, uint16(b))


# 24-bit offset in table, NULL = 0x000000
class Offset24(int, TTFType):
    fmt: str = "3c"
    sz: int = 3

    def __new__(cls: Self, b: bytes = b"\x00\x00\x00") -> Self:
        return int.__new__(cls, uint24(b))


# 32-bit offset in table, NULL = 0x00000000
class Offset32(int, TTFType):
    fmt: str = "4c"
    sz: int = 4

    def __new__(cls: Self, b: bytes = b"\x00\x00\x00\x00") -> Self:
        return int.__new__(cls, uint32(b))


# 2 16-bit uints (2nd uses only first 4 bits)
class Version16Dot16(tuple[int, int], TTFType):
    fmt: str = "4c"
    sz: int = 4

    def __new__(cls: Self, b: bytes = b"\x00\x00\x00\x00") -> Self:
        # The upper 16 bits comprise a major version number,
        # and the lower 16 bits, a minor version. Non-zero minor
        # version numbers are represented using digits 0 to 9 in
        # the highest-order nibbles of the lower 16 bits
        return tuple.__new__(cls, (b[0] << 8 + b[1], (b[2] & 0xF0) >> 4))


# An array of fixed type and length. Supports being an Array of SubTables (even with their own dynamic arrays)
class Array(tuple, TTFType):
    # Array type, the array is ill-formed if this isn't set and creation.
    # If the base Array ever gets a __typ__ value all of hell will break loose (maybe).
    __typ__: type[TTFType] = None
    __ln__: int = 0  # Array length (not byte size) 0 is a valid amount

    def __new__(cls, b: bytes = b""):
        if cls.__typ__ is None:
            raise TypeError(f"{cls} is not a fully formed Array")

        # Because the Array's TTF type might be dynamic is size
        # all we can do is iterate over them. This could be shortened to an actual
        # struct read for static arrays.
        sz = 0
        items = [None] * cls.__ln__
        for idx in range(cls.__ln__):
            items[idx] = item = cls.__typ__.read(b, sz)
            if item.sz is None or item.fmt is None:
                raise ValueError(
                    f"failed to create a fully formed ttf item of type {cls.__typ__} in {cls} from buffer {b} at offset {sz}"
                )
            sz += item.sz

        array = tuple.__new__(cls, items)
        array.fmt = "".join(item.fmt for item in array)
        array.sz = sz

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

    def __class_getitem__(cls: Self, inp: type[TTFType] | int | tuple[TTFType, int]):
        """
        To follow the convention set by the other TTF types and to reduce the
        teeny tiny boiler-plate Array delves into types metamagic to store
        the array type and size for later. This only works because
        dataclasses.Field stores the actual type. If another implimentation
        doesn't follow suit this code will not work. Also type-checker's hate this
        a lot.
        """
        if isinstance(inp, tuple):
            if cls.__typ__ is not None:
                raise ValueError(f"{Array} already has a defined type")
            elif len(inp) != 2:
                raise TypeError("{cls} only accepts up to two type arguments")
            typ, ln = inp

            if not isinstance(ln, int):
                raise TypeError(
                    "{cls} only accepts an integer length for the second argument"
                )
            elif not isinstance(typ, type):
                raise TypeError("{cls} only accepts types for the first argument")

            newcls = type(cls.__name__, cls.__bases__, dict(**cls.__dict__))
            newcls.__typ__ = typ
            newcls.__ln__ = ln

            # If the type's format and size are static then so it the array's
            if typ.sz is not None and typ.fmt is not None:
                newcls.sz = ln * typ.sz
                newcls.fmt = ln * typ.fmt
            return newcls
        elif isinstance(inp, type):
            if cls.__typ__ is not None:
                raise ValueError(f"{Array} already has a defined type")
            newcls = type(cls.__name__, cls.__bases__, dict(**cls.__dict__))
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

            # If the type's format and size are static then so it the array's
            if cls.__typ__.sz is not None and cls.__typ__.fmt is not None:
                cls.sz = inp * cls.__typ__.sz
                cls.fmt = inp * cls.__typ__.fmt
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
    def __call__(
        self, *srcs, typ: type[TTFType], buffer: bytes, offset: int = 0
    ) -> TTFType: ...


# staticEntry - Found in the table as is (default)
# dynamicEntry - Real value must be calcuated, and does not have to be in table by default


def static():
    return dataclasses.field(metadata={"entry": "static"})


def dynamic(f: DynamicFunction, *srcs, derived: bool = False):
    return dataclasses.field(
        metadata={"entry": "dynamic", "derived": derived, "srcs": srcs, "func": f}
    )


def array(src: str, derived: bool = False):
    return dynamic(_parse_semistatic_array, src, derived=derived)


def _parse_static(typ: type[TTFType], buffer: bytes, offset: int = 0):
    # Avoid boilerplater for simplest dynamic case (static) and provide default
    item = typ.read(buffer, offset)
    if item.sz is None or item.fmt is None:
        raise ValueError(f"Failed to create {typ} from buffer {buffer} at {offset}")
    return item


def _parse_semistatic_array(
    src: TTFType, typ: type[TTFType], buffer: bytes, offset: int = 0
):
    # Avoid boilerplate for the simple case where the array length is just based on another table element
    return typ[src].read(buffer, offset)


def _find_table_static(tbl: type[Table]) -> tuple[None | str, None | int]:
    # Attempt to find the static size of a table (or more likely a Record).
    sz = 0
    fmt = ""
    for field in dataclasses.fields(tbl):
        typ = field.typ
        if typ.sz is None or typ.fmt is None:
            break
        sz += typ.sz
        fmt += typ.fmt
    else:
        return fmt, sz
    return None, None


class Table(TTFType):
    __versions__: dict[TTFType, type[Table]] = None

    @classmethod
    def read(cls: Self, buffer: bytes, offset: int = 0) -> Self:
        # No versions were defined so use the default (initial definition)
        if not cls.__versions__:
            return cls._read(buffer, offset)

        version_field = dataclasses.fields(cls)[0]  # Assuming version is always first
        version_type: TTFType = version_field.type
        version = version_type.read(buffer, offset)
        print(version)
        return cls.__versions__.get(version, cls)._read(buffer, offset)

    @classmethod
    def read_version(cls: Self, v: TTFType, buffer: bytes, offset: int = 0) -> Self:
        if v not in cls.__versions__:
            raise ValueError(f"Version {v} was never defined for {cls}")
        return cls.__versions__[v]._read(buffer, offset)

    @classmethod
    def _read(cls: Self, buffer: bytes, offset: int) -> Self:
        # Many table formats have variable length arrays that make
        # using struct.unpack difficult, but each type still has it fmt.
        fields = dataclasses.fields(cls)
        values: dict[str, TTFType] = {}
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
    def version(cls: Self, v: TTFType) -> Self:
        if not isinstance(v, TTFType):
            raise ValueError(f"{v} is not a ttf type and cannot be used for versioning")

        def wrap(subcls: type[Self]):
            subcls = dataclasses.dataclass(subcls)
            cls.__versions__[v] = subcls
            return cls

        return wrap


def definition(cls: type) -> type[Table]:
    # A decorator used to define a new table.
    # Ensures that cls is a Table subclass, but
    # also allows for it to be subclassed directly.
    if not issubclass(cls, Table):
        # Clone the cls type, but makes Table as a parent class
        bases = cls.__bases__
        if bases == (object,):
            bases = ()
        cls = type(cls.__name__, bases + (Table,), dict(**cls.__dict__))
    elif cls.__versions__ is not None:
        raise ValueError(
            f"A table of type {cls} has already been defined use `{cls}.version(<x>)` instead"
        )
    cls = dataclasses.dataclass(cls)
    cls.__versions__ = {}

    # If the
    cls.fmt, cls.sz = _find_table_static(cls)
    return cls
