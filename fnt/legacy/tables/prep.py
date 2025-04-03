from fnt.types import Table, arrayEntry, propertyEntry, Array, uint8, uint32


class prep(Table):
    _length: uint32 = propertyEntry()
    program: Array[uint8] = arrayEntry("_length")
