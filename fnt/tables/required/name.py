from fnt.types import (
    definition,
    versionEntry,
    arrayEntry,
    uint16,
    Offset16,
    Array,
)


@definition
class NameRecord:
    platformID: uint16
    encodingID: uint16
    languageID: uint16
    nameID: uint16
    length: uint16
    stringOffset: Offset16


@definition
class LangTagRecord:
    length: uint16
    langTagOffset: Offset16


@definition
class name:
    version: uint16 = versionEntry()


@name.add_version(uint16.byte(0))
class name:
    version: uint16
    count: uint16
    storageOffset: Offset16
    nameRecord: Array[NameRecord] = arrayEntry("count")


@name.add_version(uint16.byte(1))
class name:
    version: uint16
    count: uint16
    storageOffset: Offset16
    nameRecord: Array[NameRecord] = arrayEntry("count")
    langTagCount: uint16
    langTagRecord: Array[LangTagRecord] = arrayEntry("langTagCount")


# TODO: provide name string reading method
