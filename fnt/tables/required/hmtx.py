from fnt.types import uint16, definition, FWORD, UFWORD, Array, dynamicEntry


@definition
class LongHorMetric:
    advanceWidth: UFWORD
    lsb: FWORD


# TODO: Find way to pass in other table values

def derive_hMetrics():
    # Todo, find way to derive this table
    pass


@definition
class hmtx:
    numOfHMetrics: 
    hMetrics: Array[LongHorMetric] = dynamicEntry(lambda: NotImplemented)
    leftSideBearing: Array[FWORD] = dynamicEntry(lambda: NotImplemented)
