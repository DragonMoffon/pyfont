from fnt.types import Table, linkedEntry, int16


class GlyphHeader(Table):
    numberOfContours: int16
    xMin: int16
    yMin: int16
    xMax: int16
    yMax: int16


class glyf(Table):
    pass
