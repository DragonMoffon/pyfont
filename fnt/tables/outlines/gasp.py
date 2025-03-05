from fnt.types import Table, arrayEntry, Array, uint16
from fnt.flags import GaspFlags


class GaspRange(Table):
    rangeMaxPPEM: uint16
    rangeGaspBehavior: uint16


class gasp(Table):
    version: uint16
    numRanges: uint16
    gaspRanges: Array[GaspRange] = arrayEntry("numRanges")
