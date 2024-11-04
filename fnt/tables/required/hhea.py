from fnt.types import uint16, int16, FWORD, UFWORD, Array, definition


@definition
class hhea:
    majorVersion: uint16
    minorVersion: uint16
    ascender: FWORD
    decender: FWORD
    lineGap: FWORD
    advanceWidthMax: UFWORD
    minLeftSideBearing: FWORD
    minRightSideBearing: FWORD
    xMaxExtent: FWORD
    caretSlopeRise: int16
    caretSlopeRun: int16
    caretOffset: int16
    RESERVED: Array[int16, 4]
    metricDataFormat: int16
    numberOfHMetrics: uint16
