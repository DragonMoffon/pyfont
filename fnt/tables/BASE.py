from fnt.types import (
    table,
    uint16,
    int16,
    offset16,
    tag,
)

@table
class BaseHeader_fmt1:
    majorVersion: uint16
    minorVersion: uint16
    horizAxisOffset: offset16
    vertAxisOffset: offset16

@table
class BaseHeader_fmt11:
    majorVersion: uint16
    minorVersion: uint16
    horizAxisOffset: offset16
    vertAxisOffset: offset16
    itemVarStoreOffset: offset16

type BaseHeader = BaseHeader_fmt1 | BaseHeader_fmt11

@table
class BaseTagList:
    baseTagCount: uint16
    baselineTags: tuple[tag, ...]

@table
class BaseScriptRecord:
    baseScriptTag: tag
    baseScriptOffset: offset16

@table
class BaseScriptList:
    baseScriptCount: uint16
    baseScriptRecords: tuple[BaseScriptRecord, ...]

@table
class BaseLangSys:
    baseLangSysTag: tag
    minMaxOffset: offset16

@table
class BaseCoord_fmt1:
    format: uint16
    coordinate: int16

@table
class BaseCoord_fmt2:
    format: uint16
    coordinate: int16
    referenceGlyph: uint16
    baseCoordPoint: uint16

@table
class BaseCoord_fmt3:
    format: uint16
    coordinate: int16
    deviceOffset: offset16


type BaseCoord = BaseCoord_fmt1 | BaseCoord_fmt2 | BaseCoord_fmt3

@table
class BaseValues:
    defaultBaselineIndex: uint16
    baseCoordCount: uint16
    baseCoordOffsets: tuple[offset16, ...]
    baseCoords: tuple[BaseCoord, ...]

@table
class FeatMinMax:
    featureTag: tag
    minCoordOffset: offset16
    maxCoordOffset: offset16
    minCoord: BaseCoord
    maxCoord: BaseCoord

@table
class MinMax:
    minCoordOffset: offset16
    maxCoordOffset: offset16
    featMinMaxCount: uint16
    featMinMaxRecords: tuple[FeatMinMax, ...]
    minCoord: BaseCoord
    maxCoord: BaseCoord


@table
class BaseScript:
    baseValuesOffset: offset16
    defaultMinMaxOffset: offset16
    baseLangSysCount: uint16
    baseLangSysRecords: tuple[BaseLangSys, ...]
    baseValues: BaseValues
    defaultMinMax: MinMax


@table
class Axis:
    baseTagListOffset: offset16
    baseScriptListOffset: offset16
    baseTagList: BaseTagList | None
    baseScriptList: BaseScriptList


@table
class BASE:
    header: BaseHeader
    horizAxis: Axis | None
    vertAxis: Axis | None
    itemVarStore: None  # TODO: impliement all of https://learn.microsoft.com/en-us/typography/opentype/spec/otvarcommonformats
    

__all__ = (
    "BASE",
    "Axis",
    "BaseScript",
    "MinMax",
    "FeatMinMax",
    "BaseValues",
    "BaseCoord",
    "BaseCoord_fmt1",
    "BaseCoord_fmt2",
    "BaseCoord_fmt3",
    "BaseHeader",
    "BaseHeader_fmt1",
    "BaseHeader_fmt11"
)