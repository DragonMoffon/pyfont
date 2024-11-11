from fnt.types import (
    definition,
    versionEntry,
    arrayEntry,
    dynamicEntry,
    Version16Dot16,
    Tag,
    uint8,
    int8,
    uint16,
    int16,
    uint32,
    int32,
    FWORD,
    UFWORD,
    Array,
    fixed,
)


@definition
class post:
    version: Version16Dot16 = versionEntry()


@post.add_version(Version16Dot16.byte(0x00010000))
class post:
    version: Version16Dot16
    italicAngle: fixed
    underlinePosition: FWORD
    uinderlineThickness: FWORD
    isFixedPitch: uint32
    minMemType42: uint32
    maxMemType42: uint32
    minMemType1: uint32
    maxMemType1: uint32


@definition
class PascalString:
    length: uint8
    chars: Array[uint8] = arrayEntry("length")


def derive_ver2_strings(
    indices: Array[uint16], typ, buffer: bytes, offset: int, sz: int
) -> Array[PascalString]:
    count = len([i for i in indices if (i - 258) >= 0])
    return typ[count].read(buffer, offset + sz)


@post.add_version(Version16Dot16.byte(0x00020000))
class post:
    version: Version16Dot16
    italicAngle: fixed
    underlinePosition: FWORD
    uinderlineThickness: FWORD
    isFixedPitch: uint32
    minMemType42: uint32
    maxMemType42: uint32
    minMemType1: uint32
    maxMemType1: uint32
    numGlyphs: uint16
    glyphNameIndex: Array[uint16] = arrayEntry("numGlyphs")
    stringData: Array[PascalString] = dynamicEntry(
        derive_ver2_strings, "glyphNameIndex"
    )


@post.add_version(Version16Dot16.byte(0x00025000))
class post:
    version: Version16Dot16
    italicAngle: fixed
    underlinePosition: FWORD
    uinderlineThickness: FWORD
    isFixedPitch: uint32
    minMemType42: uint32
    maxMemType42: uint32
    minMemType1: uint32
    maxMemType1: uint32
    numGlyphs: uint16
    offset: Array[int8] = arrayEntry("numGlyphs")


@post.add_version(Version16Dot16.byte(0x00030000))
class post:
    version: Version16Dot16
    italicAngle: fixed
    underlinePosition: FWORD
    uinderlineThickness: FWORD
    isFixedPitch: uint32
    minMemType42: uint32
    maxMemType42: uint32
    minMemType1: uint32
    maxMemType1: uint32
