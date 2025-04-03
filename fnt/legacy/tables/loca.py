from fnt.types import (
    Table,
    versionEntry,
    linkedEntry,
    dynamicEntry,
    int16,
    uint16,
    Array,
    arrayEntry,
    Offset16,
    Offset32,
)


class loca(Table):
    indexToLocFormat: int16 = linkedEntry("head", "indexToLocFormat", version=True)


@loca.add_version(int16.byte(0))
class locaShort:
    _numGlyphs: uint16 = linkedEntry("maxp", "numGlyphs")
    _count: uint16 = dynamicEntry(
        lambda v, *_: uint16.byte(v + 1), "_numGlyphs", derived=True
    )
    offsets: Array[Offset16] = arrayEntry("_count")


@loca.add_version(int16.byte(1))
class locaLong:
    _numGlyphs: uint16 = linkedEntry("maxp", "numGlyphs")
    _count: uint16 = dynamicEntry(
        lambda v, *_: uint16.byte(v + 1), "_numGlyphs", derived=True
    )
    offsets: Array[Offset32] = arrayEntry("_count")
