from fnt.types import Table, dynamicEntry, propertyEntry, Array, FWORD, uint32


class cvt(Table):
    _length: uint32 = propertyEntry()
    program: Array[FWORD] = dynamicEntry(
        lambda l, t, b, o, s: t[l // 2].read(b, o + s), "length"
    )
