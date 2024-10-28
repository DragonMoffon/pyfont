"""
definition of common dynamic functions
"""

from math import log2

from fnt.types import uint16, DynamicFunction


# Not part of actual table
def derive_count(scalar: int) -> DynamicFunction:
    return lambda countX, *_: uint16.byte(countX // scalar)


# Only safe to truncate for unsigned ints (find largest power of 2 <= s)
def derive_searchRange(scalar: int) -> DynamicFunction:
    return lambda count, *_: uint16.byte(scalar * (2 ** (int(log2(count)))))


# Is defined as log2(searchRange/scalar)
def derive_entrySelector() -> DynamicFunction:
    return lambda count, *_: uint16.byte(int(log2(count)))


def derive_rangeShift(scalar: int) -> DynamicFunction:
    return lambda count, range, *_: uint16.byte(scalar * count - range)
