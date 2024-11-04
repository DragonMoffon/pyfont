from fnt.types import definition, Version16Dot16, uint16, versionEntry


@definition
class maxp:
    version: Version16Dot16 = versionEntry()


@maxp.add_version(Version16Dot16(b"\x00\x00\x50\x00"))
class maxp:
    version: Version16Dot16
    numGlyphs: uint16


@maxp.add_version(Version16Dot16(b"\x00\x01\x00\x00"))
class maxp:
    version: Version16Dot16
    numGlyphs: uint16
    maxPoints: uint16
    maxContours: uint16
    maxCompositePoints: uint16
    maxCompositeContours: uint16
    maxZones: uint16
    maxTwilightPoints: uint16
    maxStorage: uint16
    maxFunctionDefs: uint16
    maxInstructionDefs: uint16
    maxStackElements: uint16
    maxSizeOfInstructions: uint16
    maxComponentElements: uint16
    maxComponentDepth: uint16
