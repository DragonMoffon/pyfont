from fnt.types import Table, uint8, uint32, Array, arrayEntry, linkedEntry


class fpgm(Table):
    count: uint32 = linkedEntry()  # TODO, figure out where this value comes from
    instuctions: Array[uint8] = arrayEntry("")
