from fnt.types import definition, FWORD, UFWORD, Array, dynamicEntry


@definition
class LongHorMetric:
    advanceWidth: UFWORD
    lsb: FWORD


# TODO: Find way to pass in other table values


@definition
class hmtx:
    hMetrics: Array[LongHorMetric] = dynamicEntry(lambda: NotImplemented)
    leftSideBearing: Array[FWORD] = dynamicEntry(lambda: NotImplemented)
