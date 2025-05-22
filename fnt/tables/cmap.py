from typing import Literal

from fnt.types import table, uint8, uint16, int16, uint24, uint32, offset32

__all__ = ("cmapHeader", "cmapSubtable", "cmap")


@table
class EncodingRecord:
    platformID: uint16
    encodingID: uint16
    subtableOffset: offset32


@table
class cmapHeader:
    version: uint16
    numTables: uint16
    encodingRecords: tuple[EncodingRecord, ...]


# Byte encoding table
@table
class cmapSubtable_v0:
    format: uint16
    length: uint16
    language: uint16
    glyphIdArray: tuple[uint8, ...]  # 256 items always, but that's excessive to record


@table
class cmapSubHeader:
    firstCode: uint16
    entryCount: uint16
    idDelta: int16
    idRangeOffset: int16


# High byte mapping through table
@table
class cmapSubtable_v2:
    format: uint16
    length: uint16
    language: uint16
    subHeaderKeys: tuple[uint16, ...]  # always 256 items
    subHeaders: tuple[cmapSubHeader, ...]
    glyphIdArray: tuple[uint16, ...]


# Segment mapping to delta values
@table
class cmapSubtable_v4:
    format: uint16
    length: uint16
    language: uint16
    segCountX2: uint16
    searchRange: uint16
    entrySelector: uint16
    rangeShift: uint16
    endCode: tuple[uint16, ...]
    reservePad: uint16
    startCode: tuple[uint16, ...]
    idDelta: tuple[uint16, ...]
    idRangeOffset: tuple[uint16, ...]
    glyphIdArray: tuple[uint16, ...]


# Trimmed table mapping
@table
class cmapSubtable_v6:
    format: uint16
    length: uint16
    language: uint16
    firstCode: uint16
    entryCount: uint16
    glyphIdArray: tuple[uint16, ...]


# Trimmed array
@table
class cmapSubtable_v10:
    format: uint16
    reserved: uint16
    length: uint32
    language: uint32
    startCharCode: uint32
    endCharCode: uint32
    glyphIdArray: tuple[uint16, ...]


@table
class MapGroup:
    startCharCode: uint32
    endCharCode: uint32
    startGlyphID: uint32


# mixed 16-bit and 32-bit coverage
@table
class cmapSubtable_v8:
    format: uint16
    length: uint16
    language: uint16
    is32: tuple[uint8, ...]  # Always 8192 items
    numGroups: uint32
    groups: tuple[MapGroup, ...]


# Segmented coverage
@table
class cmapSubtable_v12:
    format: uint16
    reserved: uint16
    length: uint32
    language: uint32
    numGroups: uint32
    groups: tuple[MapGroup, ...]


# Many-to-one range mappings
@table
class cmapSubtable_v13:
    format: uint16
    reserved: uint16
    length: uint32
    numGroups: uint32
    groups: tuple[MapGroup, ...]


@table
class VariationSelector:
    varSelector: uint24
    defaultUVSOffset: offset32
    nonDefaultUVSOffset: offset32


@table
class UnicodeValueRange:
    startUnicodeValue: uint24
    additionalCount: uint8


@table
class DefaultUVS:
    numUnicodeValueRanges: uint32
    ranges: tuple[UnicodeValueRange, ...]


@table
class UVSMapping:
    unicodeValue: uint24
    glyphID: uint16


@table
class NonDefaultUVS:
    numUVSMappings: uint32
    uvsMappings: tuple[UVSMapping, ...]


@table
class cmapSubtable_v14:
    format: uint16
    length: uint16
    numVarSelectorRecords: uint32
    varSelector: tuple[VariationSelector, ...]
    defaultUVS: tuple[DefaultUVS, ...]
    nonDefaultUVS: tuple[NonDefaultUVS, ...]


type cmapSubtable = Literal[  # type: ignore
    cmapSubtable_v0,
    cmapSubtable_v2,
    cmapSubtable_v4,
    cmapSubtable_v6,
    cmapSubtable_v8,
    cmapSubtable_v10,
    cmapSubtable_v12,
    cmapSubtable_v13,
    cmapSubtable_v14,
]


@table
class cmap:
    header: cmapHeader
    subTables: tuple[cmapSubtable, ...]
