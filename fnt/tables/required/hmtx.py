from fnt.types import (
    Table,
    uint16,
    FWORD,
    UFWORD,
    Array,
    dynamicEntry,
    arrayEntry,
    linkedEntry,
)


class LongHorMetric(Table):
    advanceWidth: UFWORD
    lsb: FWORD


class hmtx(Table):
    numOfHMetrics: uint16 = linkedEntry("hhea", "numberOfHMetrics")
    numGlyphs: uint16 = linkedEntry("maxp", "numGlyphs")
    diff: uint16 = dynamicEntry(
        lambda m, g, *_: uint16.byte(g - m), "numOfHMetrics", "numGlyphs"
    )
    hMetrics: Array[LongHorMetric] = arrayEntry("numOfHMetrics")
    leftSideBearing: Array[FWORD] = arrayEntry("diff")
