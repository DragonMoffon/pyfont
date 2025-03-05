from __future__ import annotations
from fnt.exceptions import (
    InvalidFieldTypeError,
    MissingVersionFieldError,
    IllformedTTFTypeError,
    TableRedefinitionError,
)
from typing import Self, Protocol, Callable, TypeVar, TYPE_CHECKING
from enum import StrEnum
import dataclasses

if TYPE_CHECKING:
    # I HATE that some tables require data from other tables,
    # I'm forcing it to be a specific field type to hopefully control
    # when this happens
    from fnt.font import Font

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
    "staticEntry",
    "dynamicEntry",
    "arrayEntry",
    "versionEntry",
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
            raise IllformedTTFTypeError(cls)

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

    def write(self) -> bytes: ...


type TTFVersion = TTFType | tuple[TTFType, ...]
TTF_T = TypeVar("TTF_T", bound=TTFType)


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
        # The F2DOT14 format consists of a signed, 2's complement integer
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
        return int.__new__(
            cls,
            (b[0] << 56)
            + (b[1] << 48)
            + (b[2] << 40)
            + (b[3] << 32)
            + (b[4] << 24)
            + (b[5] << 16)
            + (b[6] << 8)
            + b[7],
        )


# Tag of 4 8-bit uints (ASCII char) for identification
class Tag(tuple[int, int, int, int], TTFType):
    fmt: str = "4c"
    sz: int = 4

    def __new__(cls: Self, b: bytes = b"\x00\x00") -> Self:
        return tuple.__new__(cls, (b[0], b[1], b[2], b[3]))

    def __str__(self) -> str:
        return "".join(chr(v) for v in self)

    def __repr__(self) -> str:
        return f"<{self.__str__()}>"


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
        return tuple.__new__(cls, ((b[0] << 8) + b[1], (b[2] & 0xF0) >> 4))


__RAW_TYPES__: dict[int, type[TTFType]] = {}


class raw(bytes, TTFType):
    fmt: str = None
    sz: int = None

    def __new__(cls, b: bytes = b""):
        return bytes.__new__(cls, b)

    @classmethod
    def read(cls, buffer: bytes, offset: int = 0) -> Self:
        if cls.sz is None:
            raise TypeError(f"{cls} must be given a size via []")

        b = buffer[offset : offset + cls.sz]
        if len(b) < cls.sz:
            raise ValueError(
                f"buffer {buffer} with offset {offset} is to small for {cls}"
            )

        return cls(b)

    def __class_getitem__(cls, sz: int):
        if not isinstance(sz, int):
            raise ValueError(f"raw must be provided an int not {sz}")
        if cls.sz is not None:
            raise TypeError(f"This raw has already had its size set to {cls.sz}")
        if sz in __RAW_TYPES__:
            return __RAW_TYPES__[sz]

        newcls = type(f"{cls.__name__}[{sz}]", cls.__bases__, dict(**cls.__dict__))
        newcls.fmt = "c" * sz
        newcls.sz = sz
        __RAW_TYPES__[sz] = newcls

        return newcls


__ARRAY_TYPES__: dict[type[TTFType] | tuple[TTFType, int], type] = {}


# An array of fixed type and length. Supports being an Array of SubTables (even with their own dynamic arrays)
class Array(tuple, TTFType):
    # Array type, the array is ill-formed if this isn't set and creation.
    # If the base Array ever gets a __typ__ value all of hell will break loose (maybe).
    __typ__: type[TTFType] = None
    __ln__: int = 0  # Array length (not byte size) 0 is a valid amount

    def __new__(cls, b: bytes = b""):
        if cls.__typ__ is None:
            raise IllformedTTFTypeError(cls)

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
    def read(cls, buffer: bytes, offset: int = 0) -> Self:
        if cls.__typ__ is None:
            raise IllformedTTFTypeError(cls)

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
        if inp in __ARRAY_TYPES__:
            return __ARRAY_TYPES__[inp]
        elif (cls.__typ__, inp) in __ARRAY_TYPES__:
            return __ARRAY_TYPES__[(cls.__typ__, inp)]

        if isinstance(inp, tuple):
            if cls.__typ__ is not None:
                raise ValueError(f"{Array} already has a defined type")
            if len(inp) != 2:
                raise TypeError("{cls} only accepts up to two type arguments")
            typ, ln = inp

            if not isinstance(ln, int):
                raise TypeError(
                    "{cls} only accepts an integer length for the second argument"
                )
            if not isinstance(typ, type):
                raise TypeError("{cls} only accepts types for the first argument")

            newcls = type(f"{typ.__name__}[{ln}]", cls.__bases__, dict(**cls.__dict__))
            newcls.__typ__ = typ
            newcls.__ln__ = ln

            # If the type's format and size are static then so it the array's
            if typ.sz is not None and typ.fmt is not None:
                newcls.sz = ln * typ.sz
                newcls.fmt = ln * typ.fmt

            __ARRAY_TYPES__[inp] = newcls
            return newcls
        elif isinstance(inp, type):
            if cls.__typ__ is not None:
                raise ValueError(f"{Array} already has a defined type")
            newcls = type(f"{inp.__name__}[]", cls.__bases__, dict(**cls.__dict__))
            newcls.__typ__ = inp

            __ARRAY_TYPES__[inp] = newcls
            return newcls
        elif cls.__typ__ is None:
            raise IllformedTTFTypeError(cls)
        elif not isinstance(inp, int):
            raise TypeError(
                f"{cls} only accepts an integer length when partially formed"
            )
        else:
            newcls = type(
                f"{cls.__typ__.__name__}[{inp}]", cls.__bases__, dict(**cls.__dict__)
            )
            newcls.__ln__ = inp

            # If the type's format and size are static then so it the array's
            if newcls.__typ__.sz is not None and newcls.__typ__.fmt is not None:
                newcls.sz = inp * newcls.__typ__.sz
                newcls.fmt = inp * newcls.__typ__.fmt

            __ARRAY_TYPES__[(newcls.__typ__, inp)] = newcls
            return newcls
        return cls

    def __str__(self) -> str:
        if self.__typ__ is None:
            return f"Invalid[]({','.join(str(item) for item in self)})"
        return f"{self.__typ__.__name__}[{self.__ln__}]({','.join(str(item) for item in self)})"

    def __repr__(self) -> str:
        return self.__str__()


# NOTE: Due to a limitation in dataclasses' field and fields methods all values found
# in the actual table, even if used soley for derivation (or padding) must be real
# fields in the final dataclass and cannot soley be an init arg


class DynamicFunction(Protocol):
    def __call__(
        self,
        *srcs: TTFType,
        typ: type[TTFType],
        buffer: bytes,
        offset: int = 0,
        sz: int = 0,
    ) -> TTFType: ...


# staticEntry - Found in the table as is (default)
# versionEntry - Found in the table as is, and is used to determine table type.
# dynamicEntry - Real value must be calcuated, and does not have to be in table by default
# linkedEntry - Relies on values from other tables.
# arrayentry - A util form of dynamic entry that makes it easy to fetch the size defined in earlier values


class EntryType(StrEnum):
    STATIC = "static"
    DYNAMIC = "dynamic"
    LINKED = "linked"
    PROPERTY = "property"


def staticEntry() -> dataclasses.Field:
    return dataclasses.field(metadata={"entry": EntryType.STATIC, "version": False})


def versionEntry() -> dataclasses.Field:
    return dataclasses.field(metadata={"entry": EntryType.STATIC, "version": True})


def dynamicEntry(
    f: DynamicFunction, *srcs: str, derived: bool = False, version: bool = False
) -> dataclasses.Field:
    return dataclasses.field(
        metadata={
            "entry": EntryType.DYNAMIC,
            "derived": derived,
            "srcs": srcs,
            "func": f,
        }
    )


def linkedEntry(table: str, entry: str, version: bool = False) -> dataclasses.Field:
    return dataclasses.field(
        metadata={
            "entry": EntryType.LINKED,
            "derived": True,
            "table": table,
            "source": entry,
        }
    )


def propertyEntry(prop: str = "length") -> dataclasses.Field:
    return dataclasses.field(
        metadata={"entry": EntryType.PROPERTY, "derived": True, "property": prop}
    )


def arrayEntry(src: str, *, derived: bool = False) -> dataclasses.Field:
    return dynamicEntry(_parse_semistatic_array, src, derived=derived)


def _parse_static(
    typ: type[TTF_T], buffer: bytes, offset: int = 0, sz: int = 0
) -> TTF_T:
    # Avoid boilerplater for simplest dynamic case (static) and provide default
    item = typ.read(buffer, offset + sz)
    if item.sz is None or item.fmt is None:
        raise ValueError(
            f"Failed to create {typ} from buffer {buffer} at {offset} + {sz}"
        )
    return item


def _parse_semistatic_array(
    src: TTFType, typ: type[TTF_T], buffer: bytes, offset: int = 0, sz: int = 0
) -> TTF_T:
    # Avoid boilerplate for the simple case where the array length is just based on another table element
    return typ[src].read(buffer, offset + sz)


def _find_table_static(tbl: type[Table]) -> tuple[None | str, None | int]:
    # Attempt to find the static size of a table (or more likely a Record).
    sz = 0
    fmt = ""
    for field in dataclasses.fields(tbl):
        typ = field.type
        if typ.sz is None or typ.fmt is None:
            break
        sz += typ.sz
        fmt += typ.fmt
    else:
        return fmt, sz
    return None, None


def _make_into_table(cls: type) -> type[Table]:
    if issubclass(cls, Table):
        return cls

    # Clone the cls type, but with Table as a parent class
    bases = cls.__bases__
    if bases == (object,):
        bases = ()
    return type(
        cls.__name__,
        (
            *bases,
            Table,
        ),
        dict(**cls.__dict__),
    )


class TableRecord(Protocol):
    tableTag: Tag
    checksum: uint32
    offset: Offset32
    length: uint32


class Definition(type):
    def __new__(cls, name, bases, dct):
        table = type.__new__(cls, name, bases, dct)
        if name == "Table":
            return table

        table = dataclasses.dataclass(table)

        table.__versions__ = {}

        table.fmt, table.sz = _find_table_static(table)
        return table


class Table(TTFType, metaclass=Definition):
    __versions__: dict[TTFType, type[Table]] = None
    __selectors__: tuple[
        (TTFVersion, Callable[[TTFVersion, TTFVersion], bool, type[Table]])
    ] = ()

    def __class_getitem__(cls, version: TTFVersion) -> type[Table]:
        if not isinstance(version, TTFType) and len(version) == 1:
            version = version[0]

        if cls.__versions__ is None:
            raise TypeError("Cannot get a table version from a version")

        if version not in cls.__versions__:
            for v, c, ver in cls.__selectors__:
                if c(version, v):
                    return ver
            # This will also fire for tables that have no versions defined, but that's
            # fine checking for an empty version dict here is redundant.
            raise ValueError(f"{version} has not been defined as a version of {cls}")

        return cls.__versions__[version]

    def __getitem__(self, entry: str) -> TTFType:
        # TODO: Add strictness when it comes to different table versions
        return getattr(self, entry)

    @classmethod
    def find_version(cls: Self, buffer: bytes, offset: int = 0) -> type[Table]:
        # No versions were defined so use the default (initial definition)
        # Or this is a version so it won't have a defined version dictionary
        if not cls.__versions__ and not cls.__selectors__:
            return cls

        # We need to get the version to delegate to the correct defintion
        # of the table. Which could be multiple fields so we have to find them
        # all and the offsets to read with.
        obj = cls._read(buffer, offset)
        version = []
        for field in dataclasses.fields(cls):
            if field.metadata.get("version", False):
                version.append(obj[field.name])

        if not version:
            # if no version values were parsed then the table definition is lacking
            # any version info, but has versions defined.
            raise MissingVersionFieldError(cls)

        return cls[*version]

    @classmethod
    def parse(cls: Self, record: TableRecord, font: Font, buffer: btyes) -> Self:
        entries: dict[str, TTFType] = {}
        fmt = ""  # Table's final struct fmt
        sz = 0  # Table's final byte size, Also used as the rolling offset
        offset = record.offset

        cls = cls.find_version(buffer, record.offset)

        for field in dataclasses.fields(cls):
            typ = field.type
            name = field.name
            match field.metadata.get("entry", EntryType.STATIC):
                case EntryType.STATIC:
                    # This entry can be read as-is from the buffer
                    value = _parse_static(typ, buffer, offset + sz)
                    entries[name] = value
                    sz += value.sz
                    fmt += value.fmt
                case EntryType.DYNAMIC:
                    # This entry has to be modified/derived instead of the raw value
                    derived = field.metadata.get("derived", False)
                    func = field.metadata.get("func", _parse_static)
                    values = (entries[src] for src in field.metadata.get("srcs", ()))
                    value = func(*values, typ, buffer, offset, sz)
                    entries[name] = value
                    if not derived:
                        # If the entry was actually found in the table then we need to
                        # offset the buffer, and add it to the format string.
                        sz += value.sz
                        fmt += value.fmt
                case EntryType.LINKED:
                    # this entry comes from another table rather than the buffer
                    source = field.metadata["source"]
                    table = font.get_table(field.metadata["table"])
                    entries[name] = table[source]
                case EntryType.PROPERTY:
                    # this entry comes from the table record or font.
                    prop = field.metadata.get("property", "length")
                    value = uint32.byte(0)
                    if prop == "length":
                        value = record.length
                    entries[name] = value
                case entry:
                    raise InvalidFieldTypeError(entry)

        obj = cls(**entries)
        obj.fmt = fmt
        obj.sz = sz

        return obj

    @classmethod
    def read(cls: Self, buffer: bytes, offset: int = 0) -> Self:
        cls = cls.find_version(buffer, offset)
        return cls._read(buffer, offset)

    @classmethod
    def _read(cls: Self, buffer, offset: int = 0) -> Self:
        entries: dict[str, TTFType] = {}
        fmt = ""  # Table's final struct fmt
        sz = 0  # Table's final byte size, Also used as the rolling offset

        for field in dataclasses.fields(cls):
            typ = field.type  # Metamagic of dataclasses.Field stores the type
            name = field.name  # Name of the Field from the dataclass def
            match field.metadata.get("entry", EntryType.STATIC):
                case EntryType.STATIC:
                    # This entry can be read as-is from the buffer
                    item = _parse_static(typ, buffer, offset + sz)
                    entries[name] = item
                    sz += item.sz
                    fmt += item.fmt
                case EntryType.DYNAMIC:
                    # This entry has to be modified/derived instead of the raw value
                    derived = field.metadata.get("derived", False)
                    srcs = (entries[src] for src in field.metadata.get("srcs", ()))
                    func = field.metadata.get("func", _parse_static)
                    item = func(*srcs, typ, buffer, offset, sz)
                    entries[name] = item
                    if not derived:
                        # If the entry was actually found in the table then we need to
                        # offset the buffer, and add it to the format string.
                        sz += item.sz
                        fmt += item.fmt
                case entry:
                    raise InvalidFieldTypeError(entry)

        obj = cls(**entries)
        obj.fmt = fmt
        obj.sz = sz

        return obj

    @classmethod
    def add_version(
        cls: Self,
        v: TTFVersion,
        c: Callable[[TTFVersion, TTFVersion], bool] | None = None,
    ) -> Self:
        if not isinstance(v, TTFType | tuple):
            raise ValueError(f"{v} is not a ttf type and cannot be used for versioning")
        if cls.__versions__ is None:
            raise TypeError(f"Cannot create a version from another version of {cls}")

        # If the table has versions then the base table has indeterminant size and fmt
        cls.fmt = None
        cls.sz = None

        def wrap(subcls: type) -> Self:
            # Update the version to be a Table, and a dataclass
            subcls = _make_into_table(subcls)
            subcls.__versions__ = None
            if c is None:
                cls.__versions__[v] = subcls
            else:
                cls.__selectors__ = (*cls.__selectors__, (v, c, subcls))

            # Helps with typing when needed
            if subcls.__name__ != cls.__name__:
                return subcls
            return cls

        return wrap


def definition(cls: type) -> type[Table]:
    # A decorator used to define a new table.
    # Ensures that cls is a Table subclass, but
    # also allows for it to be subclassed directly.
    return _make_into_table(cls)
