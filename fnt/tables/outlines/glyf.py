from typing import Self
from fnt.types import (
    Table,
    linkedEntry,
    versionEntry,
    arrayEntry,
    dynamicEntry,
    Array,
    int8,
    uint8,
    int16,
    uint16,
    F2DOT14,
)
from fnt.flags import SimpleGlyphFlags, CompositeGlyphFlags


class Glyph(Table):
    numberOfContours: int16 = versionEntry()


def derive_array_sizes(
    endPtsOfContours: Array[uint16],
    typ: Array[uint16, 3],
    buffer: bytes,
    offset: int = 0,
    sz: int = 0,
) -> Array[uint16, 3]:
    if len(endPtsOfContours) == 0:
        return Array[uint16, 3](b"\00\00\00\00\00\00")

    _repeat = 0

    _x_size = 0
    _y_size = 0
    _f_size = 0

    for point in range(endPtsOfContours[-1] + 1):
        if _repeat > 0:
            _repeat -= 1
            continue

        flag = uint8.read(buffer, offset + sz + _f_size)

        # When the short flag is triggered the
        # coordniate is always an uint8
        # when the sign flag is triggered then
        # the coordinate is copied and so isn't included
        # when neither is triggered then its an int16
        if flag & SimpleGlyphFlags.X_SHORT_VECTOR:
            _x_size += 1
        elif not flag & SimpleGlyphFlags.X_IS_SAME_OR_POSITIVE_X_SHORT_VECTOR:
            _x_size += 2

        if flag & SimpleGlyphFlags.Y_SHORT_VECTOR:
            _y_size += 1
        elif not flag & SimpleGlyphFlags.Y_IS_SAME_OR_POSITIVE_Y_SHORT_VECTOR:
            _y_size += 2

        _f_size += 1
        if flag & SimpleGlyphFlags.REPEAT_FLAG:
            _f_size += 1

    return Array[uint16, 3](
        _f_size.to_bytes(2) + _x_size.to_bytes(2) + _y_size.to_bytes(2)
    )


def parse_flag_array(
    pointLength: Array[uint16, 3],
    typ: Array[uint8],
    buffer: bytes,
    offset: int = 0,
    sz: int = 0,
):
    return typ[pointLength[0]].read(buffer, offset + sz)


def parse_x_array(
    pointLength: Array[uint16, 3],
    typ: Array[uint8],
    buffer: bytes,
    offset: int = 0,
    sz: int = 0,
):
    return typ[pointLength[1]].read(buffer, offset + sz)


def parse_y_array(
    pointLength: Array[uint16, 3],
    typ: Array[uint8],
    buffer: bytes,
    offset: int = 0,
    sz: int = 0,
):
    return typ[pointLength[2]].read(buffer, offset + sz)


@Glyph.add_version(int16.byte(0), lambda a, b: a >= b)
class SimpleGlyphHeader(Table):
    numberOfContours: int16
    xMin: int16
    xMax: int16
    yMin: int16
    yMax: int16
    endPtsOfContours: Array[uint16] = arrayEntry("numberOfContours")
    instructionLength: uint16
    instructions: Array[uint8] = arrayEntry("instructionLength")
    pointLength: Array[uint16, 3] = dynamicEntry(
        derive_array_sizes, "endPtsOfContours", derived=True
    )

    # Work has to be done using the flags to have these be actually useful points
    # pyfont doesn't do this work.
    flags: Array[uint8] = dynamicEntry(parse_flag_array, "pointLength")
    xCoordinates: Array[uint8] = dynamicEntry(parse_x_array, "pointLength")
    yCoordinates: Array[uint8] = dynamicEntry(parse_y_array, "pointLength")


class CompositeGlyphDescription(Table):
    flags: uint16 = versionEntry()


def contains(a, b):
    return (a & b) == b


s16 = CompositeGlyphFlags.ARG_1_AND_2_ARE_WORDS | CompositeGlyphFlags.ARGS_ARE_XY_VALUES
us16 = CompositeGlyphFlags.ARG_1_AND_2_ARE_WORDS
s8 = CompositeGlyphFlags.ARGS_ARE_XY_VALUES
us8 = uint16.byte(0x0000)


@CompositeGlyphDescription.add_version(
    s16 | CompositeGlyphFlags.WE_HAVE_A_SCALE, contains
)
class CompositeGlyphDescription:
    flags: uint16
    glyphIndex: uint16
    xOffset: int16
    yOffset: int16
    scale: F2DOT14


@CompositeGlyphDescription.add_version(
    us16 | CompositeGlyphFlags.WE_HAVE_A_SCALE, contains
)
class CompositeGlyphDescription:
    flags: uint16
    glyphIndex: uint16
    xOffset: uint16
    yOffset: uint16
    scale: F2DOT14


@CompositeGlyphDescription.add_version(
    s8 | CompositeGlyphFlags.WE_HAVE_A_SCALE, contains
)
class CompositeGlyphDescription:
    flags: uint16
    glyphIndex: uint16
    xOffset: int8
    yOffset: int8
    scale: F2DOT14


@CompositeGlyphFlags.add_version(us8 | CompositeGlyphFlags.WE_HAVE_A_SCALE, contains)
class CompositeGlyphDescription:
    flags: uint16
    glyphIndex: uint16
    xOffset: uint8
    yOffset: uint8
    scale: F2DOT14


@CompositeGlyphDescription.add_version(
    s16 | CompositeGlyphFlags.WE_HAVE_AN_X_AND_Y_SCALE, contains
)
class CompositeGlyphDescription:
    flags: uint16
    glyphIndex: uint16
    xOffset: int16
    yOffset: int16
    xScale: F2DOT14
    yScale: F2DOT14


@CompositeGlyphDescription.add_version(
    us16 | CompositeGlyphFlags.WE_HAVE_AN_X_AND_Y_SCALE, contains
)
class CompositeGlyphDescription:
    flags: uint16
    glyphIndex: uint16
    xOffset: uint16
    yOffset: uint16
    xScale: F2DOT14
    yScale: F2DOT14


@CompositeGlyphDescription.add_version(
    s8 | CompositeGlyphFlags.WE_HAVE_AN_X_AND_Y_SCALE, contains
)
class CompositeGlyphDescription:
    flags: uint16
    glyphIndex: uint16
    xOffset: int8
    yOffset: int8
    xScale: F2DOT14
    yScale: F2DOT14


@CompositeGlyphFlags.add_version(
    us8 | CompositeGlyphFlags.WE_HAVE_AN_X_AND_Y_SCALE, contains
)
class CompositeGlyphDescription:
    flags: uint16
    glyphIndex: uint16
    xOffset: uint8
    yOffset: uint8
    xScale: F2DOT14
    yScale: F2DOT14


@CompositeGlyphDescription.add_version(
    s16 | CompositeGlyphFlags.WE_HAVE_A_TWO_BY_TWO, contains
)
class CompositeGlyphDescription:
    flags: uint16
    glyphIndex: uint16
    xOffset: int16
    yOffset: int16
    xScale: F2DOT14
    scale01: F2DOT14
    scale10: F2DOT14
    yScale: F2DOT14


@CompositeGlyphDescription.add_version(
    us16 | CompositeGlyphFlags.WE_HAVE_A_TWO_BY_TWO, contains
)
class CompositeGlyphDescription:
    flags: uint16
    glyphIndex: uint16
    xOffset: uint16
    yOffset: uint16
    xScale: F2DOT14
    scale01: F2DOT14
    scale10: F2DOT14
    yScale: F2DOT14


@CompositeGlyphDescription.add_version(
    s8 | CompositeGlyphFlags.WE_HAVE_A_TWO_BY_TWO, contains
)
class CompositeGlyphDescription:
    flags: uint16
    glyphIndex: uint16
    xOffset: int8
    yOffset: int8
    xScale: F2DOT14
    scale01: F2DOT14
    scale10: F2DOT14
    yScale: F2DOT14


@CompositeGlyphFlags.add_version(
    us8 | CompositeGlyphFlags.WE_HAVE_A_TWO_BY_TWO, contains
)
class CompositeGlyphDescription:
    flags: uint16
    glyphIndex: uint16
    xOffset: uint8
    yOffset: uint8
    xScale: F2DOT14
    scale01: F2DOT14
    scale10: F2DOT14
    yScale: F2DOT14


def parse_glyph_descriptions(
    typ: Array[CompositeGlyphDescription], buffer: bytes, offset: int = 0, sz: int = 0
):
    obj = CompositeGlyphDescription.read(buffer, offset + sz)
    sz += obj.sz
    children = [obj]
    while obj.flags & CompositeGlyphFlags.MORE_COMPONENTS:
        obj = CompositeGlyphDescription.read(buffer, offset + sz)

    return typ[len(children)].force(*children)


def parse_instruction_length(
    children: Array[CompositeGlyphDescription],
    typ: type[uint16],
    buffer: bytes,
    offset: int = 0,
    sz: int = 0,
):
    if children and children[-1].flags & CompositeGlyphFlags.WE_HAVE_INSTRUCTIONS:
        return typ.read(buffer, offset + sz)
    return typ.byte(0x00)


@Glyph.add_version(int16.byte(0, signed=True), lambda a, b: a < b)
class CompositeGlyph(Table):
    numberOfContours: int16
    xMin: int16
    xMax: int16
    yMin: int16
    yMax: int16
    children: Array[CompositeGlyphDescription] = dynamicEntry(parse_glyph_descriptions)
    instructionLength: uint16 = dynamicEntry(parse_instruction_length, "children")
    instructions: Array[uint8] = arrayEntry("instructionLength")


def parse_glyphs(
    count: uint16,
    offsets: Array,
    multiplier: int16,
    typ: Array[Glyph],
    buffer: bytes,
    offset: int = 0,
    sz: int = 0,
):
    multiplier = 1 if multiplier else 2
    glyphs = []
    for glyph_id in range(count):
        glyph_offset = offsets[glyph_id] * multiplier
        size = (offsets[glyph_id + 1] - offsets[glyph_id]) * multiplier
        if size == 0:
            continue
        glyph = Glyph.read(buffer, offset + glyph_offset)
        sz += size
        glyphs.append(glyph)

    return Array[Glyph, len(glyphs)].force(*glyphs)


class glyf(Table):
    _numGlyphs: uint16 = linkedEntry("maxp", "numGlyphs")
    _multiplier: int16 = linkedEntry("head", "indexToLocFormat")
    _offsets: Array = linkedEntry("loca", "offsets")
    glyphs: Array[Glyph] = dynamicEntry(
        parse_glyphs, "_numGlyphs", "_offsets", "_multiplier"
    )
