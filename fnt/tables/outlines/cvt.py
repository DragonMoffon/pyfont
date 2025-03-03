from fnt.types import Table, Array, uint32, FWORD, arrayEntry, linkedEntry


class cvt(Table):
    count: uint32 = linkedEntry()  # TODO, figure out where this value comes from
    variables: Array[FWORD] = arrayEntry("count")
