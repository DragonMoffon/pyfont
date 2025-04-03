from fnt.types import (
    Table,
    uint16,
    int16,
    uint32,
    fixed,
    LONGDATETIME,
)


class head(Table):
    majorVersion: uint16
    minorVersion: uint16
    fontRevision: fixed
    checksumAdjustment: uint32
    magicNumber: uint32
    flags: uint16
    unitsPerEm: uint16
    created: LONGDATETIME
    modified: LONGDATETIME
    xMin: int16
    yMin: int16
    xMax: int16
    yMax: int16
    macStyle: uint16
    lowestRecPPEM: uint16
    fontDirectionHint: int16
    indexToLocFormat: int16
    glyphDataFormat: int16
