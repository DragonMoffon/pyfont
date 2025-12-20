"""
There are a series of common layout tables used by the
GSUB, GPOS, BASE, JSTF, GDEF, and MATH tables.
they are described at https://learn.microsoft.com/en-us/typography/opentype/spec/chapter2
"""
from fnt.types import (
    table,
    uint8,
    int8,
    uint16,
    int16,
    uint32,
    offset16,
    offset32,
    UFWORD,
    FWORD,
    fixed,
    F2DOT14,
    LONGDATETIME,
    tag,
    version16dot16,
    int8x16,
    int8x6,
    int8x8
)

@table
class ScriptRecord:
    scriptTag: tag
    scriptOffset: offset16

@table
class ScriptList:
    scriptCount: uint16
    scriptRecords: tuple[ScriptRecord, ...]

@table
class LangSysRecord:
    langSysTag: tag
    langSysOffset: offset16

@table
class Script:
    defaultLangOffset: offset16 | None # Nullable
    langSysCount: uint16
    langSysRecords: tuple[LangSysRecord, ...]

@table
class LangSys:
    lookupOrderOffset: offset16
    requiredFeatureIndex: uint16
    featureIndexCount: uint16
    featureIndices: tuple[uint16, ...]

@table
class FeatureRecord:
    featureTag: tag
    featureoffset: offset16

@table
class FeatureList:
    featureCount: uint16
    featureRecords: tuple[FeatureRecord, ...]