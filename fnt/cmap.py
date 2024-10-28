"""
This file defines everything described in:
https://learn.microsoft.com/en-us/typography/opentype/spec/cmap

This was also the table that most of types.py was working around.
Hopefully it was diverse enough to support everything.
"""

from fnt.types import (
    definition,
    uint8,
    uint16,
    int16,
    uint32,
    uint24,
    Offset32,
    Array,
    arrayEntry,
    dynamicEntry,
    versionEntry,
)
from fnt.dynamic import (
    derive_entrySelector,
    derive_searchRange,
    derive_count,
    derive_rangeShift,
)


@definition
class EncodingRecord:
    platformID: uint16
    encodingID: uint16
    subtableOffset: Offset32


@definition
class cmapHeader:
    version: uint16
    numTables: uint16
    encodingRecords: Array[EncodingRecord] = arrayEntry("numTables")


@definition
class cmapSubHeader:
    firstCode: uint16
    entryCount: uint16
    idDelta: int16
    idRangeOffset: int16


@definition
class cmapSubtable:
    format: uint16 = versionEntry()


# Byte encoding table
@cmapSubtable.add_version(uint16.byte(0))
class cmapSubtable:
    format: uint16
    length: uint16
    language: uint16
    glyphIdArray: Array[uint8, 256]


def derive_subHeaders(
    keys: Array[uint16, 256],
    typ: Array[cmapSubHeader],
    buffer: bytes,
    offset: int = 0,
    sz: int = 0,
):
    k_max = max(keys // 8) + 1  # Get the max possible index for the subHeaders
    return typ[k_max].get(buffer, offset + sz)


def derive_fmt2_glyphIdArray(
    subHeaders: Array[cmapSubHeader],
    typ: Array[uint16],
    buffer: bytes,
    offset: int = 0,
    sz: int = 0,
):
    # Get the max possible index for the glyphID based on the subHeaders
    j_max = (
        max(sub_header.firstCode + sub_header.entryCount for sub_header in subHeaders)
        + 1
    )

    return typ[j_max + 1].get(buffer, offset + sz)


# High byte mapping through table
@cmapSubtable.add_version(uint16.byte(2))
class cmapSubtable:
    format: uint16
    length: uint16
    language: uint16
    subHeaderKeys: Array[uint16, 256]
    subHeaders: Array[cmapSubHeader] = dynamicEntry(derive_subHeaders, "subHeaderKeys")
    glyphIdArray: Array[uint16] = dynamicEntry(derive_fmt2_glyphIdArray, "subHeaders")


def derive_fmt4_glpyhIdArray(count, length, typ, buffer, offset, sz):
    # The complexities of calculating the correct length for the glyphIdArray
    # mean it is just easier to use the byte length

    non_array_sz = 8 * uint16.sz
    array_sz = 4 * uint16.sz * count
    ln = (length - non_array_sz - array_sz) // 2

    return typ[ln].read(buffer, offset + sz)


def fmt4_character_from_glyph(glyph, encoding: cmapSubtable):
    raise NotImplementedError("This logic is currently wrong don't use")

    for check_idx in range(encoding.segCount):
        start_code = encoding.startCode[check_idx]
        end_code = encoding.endCode[check_idx]
        id_delta = encoding.idDelta[check_idx]
        id_offset = encoding.idRangeOffset[check_idx]

        # Because we are trusting that the glyphIdx is in the 0x0000 - 0xFFFF the mod
        # isn't lossy
        maybe_idx = (glyph - id_delta) % 0xFFFF
        if id_offset != 0:
            # The offset isn't zero so we need to simulate what we would do
            # using point arithmatic.
            shift = id_offset // 2 + check_idx - encoding.segCount
            if 0 <= maybe_idx - shift <= (end_code - start_code):
                return chr(maybe_idx + start_code - shift)
        elif start_code <= maybe_idx <= end_code:
            return chr(maybe_idx)

    return chr(0)  # Null character


def fmt4_glyph_from_character(character, encoding: cmapSubtable):
    o = ord(character)
    if o > 0xFFFF:
        raise ValueError(
            f"<{character}> has ord({ord(character)}) which is too large for format-4"
        )

    check_idx = -1
    for idx, code in enumerate(encoding.endCode):
        if o <= code:
            check_idx = idx
            break
    else:
        raise ValueError("the endCode array doesn't end with 0xFFFF")

    start_code = encoding.startCode[check_idx]
    id_delta = encoding.idDelta[check_idx]
    id_offset = encoding.idRangeOffset[check_idx]
    if o < start_code:
        return 0
    elif id_offset != 0:
        id_idx = id_offset // 2 + check_idx - encoding.segCount + (o - start_code)
        if encoding.glyphIdArray[id_idx] == 0:
            return 0
        glyph_idx = encoding.glyphIdArray[id_idx]
    else:
        glyph_idx = o

    return (glyph_idx + id_delta) % 0xFFFF


# Segment mapping to delta values
@cmapSubtable.add_version(uint16.byte(4))  # i.e. Format 4
class cmapSubtable:
    format: uint16
    length: uint16
    language: uint16
    segCountX2: uint16
    segCount: uint16 = dynamicEntry(derive_count(2), "segCountX2", derived=True)
    searchRange: uint16 = dynamicEntry(derive_searchRange(2), "segCount")
    entrySelector: uint16 = dynamicEntry(derive_entrySelector(), "segCount")
    rangeShift: uint16 = dynamicEntry(derive_rangeShift(2), "segCount", "searchRange")
    endCode: Array[uint16] = arrayEntry("segCount")
    reservePad: uint16
    startCode: Array[uint16] = arrayEntry("segCount")
    idDelta: Array[uint16] = arrayEntry("segCount")
    idRangeOffset: Array[uint16] = arrayEntry("segCount")
    glyphIdArray: Array[uint16] = dynamicEntry(
        derive_fmt4_glpyhIdArray, "segCount", "length"
    )


# Shared by fmt 8 and 12 (and 13 under another name)
class MapGroup:
    startCharCode: uint32
    endCharCode: uint32
    startGlyphID: uint32


SequentialMapGroup = definition(MapGroup)
ConstantMapGroup = definition(MapGroup)


# Trimmed table mapping
@cmapSubtable.add_version(uint16.byte(6))
class cmapSubtable:
    format: uint16
    length: uint16
    language: uint16
    firstCode: uint16
    entryCount: uint16
    glyphIdArray: Array[uint16] = arrayEntry("entryCount")


# mixed 16-bit and 32-bit coverage
@cmapSubtable.add_version(uint16.byte(8))
class cmapSubtable:
    format: uint16
    length: uint16
    language: uint16
    is32: Array[uint8, 8192]
    numGroups: uint32
    groups: Array[SequentialMapGroup] = arrayEntry("numGroups")


# Segmented coverage
@cmapSubtable.add_version(uint16.byte(12))
class cmapSubtable:
    format: uint16
    reserved: uint16
    length: uint32
    language: uint32
    numGroups: uint32
    groups: Array[SequentialMapGroup] = arrayEntry("numGroups")


# Many-to-one range mappings
@cmapSubtable.add_version(uint16.byte(13))
class cmapSubtable:
    format: uint16
    reserved: uint16
    length: uint32
    numGroups: uint32
    groups: Array[ConstantMapGroup] = arrayEntry("numGroups")


# Trimmed array
@cmapSubtable.add_version(uint16.byte(10))
class cmapSubtable:
    format: uint16
    reserved: uint16
    length: uint32
    language: uint32
    startCharCode: uint32
    endCharCode: uint32
    glyphIdArray: Array[uint16] = dynamicEntry(
        lambda s, e, typ, buffer, offset: typ[e - s + 1].read(buffer, offset),
        "startCharCode",
        "endCharCode",
    )


# Used by fmt 14
@definition
class VariationSelector:
    varSelector: uint24
    defaultUVSOffset: Offset32
    nonDefaultUVSOffset: Offset32


@definition
class UnicodeValueRange:
    startUnicodeValue: uint24
    additionalCount: uint8


@definition
class DefaultUVS:
    numUnicodeValueRanges: uint32
    ranges: Array[UnicodeValueRange] = arrayEntry("numUnicodeValueRanges")


@definition
class UVSMapping:
    unicodeValue: uint24
    glyphID: uint16


@definition
class NonDefaultUVS:
    numUVSMappings: uint32
    uvsMappings: Array[UVSMapping] = arrayEntry("numUVSMappings")


def derive_fmt14_UVSDefaultArray(
    varSelector, typ, buffer, offset: int = 0, sz: int = 0
):
    # The Array type expects a packed Contigous buffer, so the byte array needs to be
    # constructed
    byterange = b""
    count = 0
    for selector in varSelector:
        o = selector.defaultUVSOffset
        if o == 0:
            continue
        count += 1

        # The first value of the sub table is a uint32 of the count so this is
        # the most reliable method
        ln = uint32.read(buffer, offset + o)
        sz = ln * (uint24.sz + uint8.sz) + uint32.sz
        byterange += buffer[offset + o : offset + o + sz]
    return typ[count].read(byterange, 0)


def derive_fmt14_UVSNonDefaultArray(
    varSelector, typ, buffer, offset: int = 0, sz: int = 0
):
    # The Array type expects a packed Contigous buffer, so the byte array needs to be
    # constructed
    byterange = b""
    count = 0
    for selector in varSelector:
        o = selector.nonDefaultUVSOffset
        if o == 0:
            continue
        count += 1

        ln = uint32.read(buffer, offset + o)
        sz = ln * (uint24.sz + uint16.sz) + uint32.sz
        byterange += buffer[offset + o : offset + o + sz]
    return typ[count].read(byterange, 0)


# Unicode variation sequences
@cmapSubtable.add_version(uint16.byte(14))
class cmapSubtable:
    format: uint16
    length: uint32
    numVarSelectorRecords: uint32
    varSelector: Array[VariationSelector] = arrayEntry("numVarSelectorRecords")
    # Even though they aren't contiguous the varSelector array gives all the info needed to load the UVS tables.
    defaultUVS: Array[DefaultUVS] = dynamicEntry(
        derive_fmt14_UVSDefaultArray, "varSelector"
    )
    nonDefaultUVS: Array[NonDefaultUVS] = dynamicEntry(
        derive_fmt14_UVSNonDefaultArray, "varSelector"
    )
