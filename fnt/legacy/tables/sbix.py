from fnt.types import (
    Table,
    uint8,
    uint16,
    int16,
    uint32,
    Offset32,
    Tag,
    Array,
    arrayEntry,
    dynamicEntry,
    linkedEntry,
)


class sbixHeader(Table):
    version: uint16
    flags: uint16
    numStrikes: uint32
    strikeOffsets: Array[Offset32] = arrayEntry("numStrikes")


class Strike(Table):
    ppem: uint16
    ppi: uint16
    glyphDataOffsets: Array[Offset32]


class Glyph:
    originOffsetX: int16
    originOffsetY: int16
    graphicType: Tag
    data: Array[uint8] = dynamicEntry()


def derive_strikes(
    header: sbixHeader,
    count: uint16,
    typ: Array[Strike],
    buffer: bytes,
    offset: int = 0,
    sz: int = 0,
):
    class Strike(Table):
        ppem: uint16
        ppi: uint16
        glyphDataOffsets: Array[Offset32, count + 1]

    strikes = []
    for sub_offset in header.strikeOffsets:
        strikes.append(Strike.read(buffer, offset, sub_offset))

    return typ.force(*strikes)


class sbix(Table):
    _count: uint16 = linkedEntry("maxp", "numGlyphs")
    header: sbixHeader
    strikes: Array[Strike] = dynamicEntry(derive_strikes, "header", "_count")
