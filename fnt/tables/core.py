from fnt.types import (
    definition,
    uint16,
    uint32,
    Offset32,
    Tag,
    Array,
    arrayEntry,
    dynamicEntry,
    versionEntry,
)
from fnt.dynamic import derive_entrySelector, derive_searchRange, derive_rangeShift


@definition
class TableRecord:
    tableTag: Tag
    checksum: uint32
    offset: Offset32
    length: uint32


@definition
class tableDirectory:
    sfntVersion: uint32
    numTables: uint16
    searchRange: uint16 = dynamicEntry(derive_searchRange(16), "numTables")
    entrySelector: uint16 = dynamicEntry(derive_entrySelector(), "numTables")
    rangeShift: uint16 = dynamicEntry(derive_rangeShift(16), "numTables", "searchRange")
    tableRecords: Array[TableRecord] = arrayEntry("numTables")


@definition
class TTCHeader:
    ttcTag: Tag  # Dud value in the base def but here for padding
    majorVersion: uint16 = versionEntry()
    minorVersion: uint16 = versionEntry()


@TTCHeader.add_version((uint16.byte(1), uint16.byte(0)))
class TTCHeader:
    ttcTag: Tag
    majorVersion: uint16
    minorVersion: uint16
    numFonts: uint32
    tableDirectoryOffsets: Array[Offset32] = arrayEntry("numFonts")


@TTCHeader.add_version((uint16.byte(1), uint16.byte(0)))
class TTCHeader:
    ttcTag: Tag
    majorVersion: uint16
    minorVersion: uint16
    numFonts: uint32
    tableDirectoryOffsets: Array[Offset32] = arrayEntry("numFonts")
    dsigTag: uint32
    dsigLength: uint32
    dsigOffset: Offset32
