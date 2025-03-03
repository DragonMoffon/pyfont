from fnt.types import Table
from .core import TableRecord, tableDirectory, TTCHeader

# Required
from .required.cmap import cmap, cmapHeader, cmapSubHeader, cmapSubtable, EncodingRecord
from .required.head import head
from .required.hhea import hhea
from .required.hmtx import hmtx
from .required.maxp import maxp
from .required.name import name, LangTagRecord, NameRecord
from .required.OS2 import OS2
from .required.post import post

# TrueType Outlines

# TODO

# CFF Outlines

# TODO

# SVG Outlines

from .outlines.SVG import SVG, SVGDocumentRecord

# Bitmap Glyphs

# TODO

# Typographic Tables

# TODO

# Font Variations

# TODO

# Other Tables

# TODO

TABLES: dict[str, type[Table]] = {
    # Required
    cmap.__name__: cmap,
    head.__name__: head,
    hhea.__name__: hhea,
    hmtx.__name__: hmtx,
    maxp.__name__: maxp,
    name.__name__: name,
    OS2.__name__: OS2,
    "OS/2": OS2,
    post.__name__: post,
    # True Type Outlines
    # CFF Outlines
    # SVG Outlines
    SVG.__name__: SVG,
    "SVG ": SVG,
    # Bitmap Glyphs
    # Typographic Tables
    # OpenType Font Variations
    # Other
}


"""
True Type Tables:
    acnt (accent attachment)
    ankr (anchor point)
    avar (axis variation)
    bdat (bitmap data)
    bhed (bitmap font header)
    bloc (bitmap location)
    bsln (baseline)
    cvar (CVT variation)
    cvt (control value)
    EBSC (embedded bitmap scaling control)
    fdsc (font descriptor)
    feat (layout feature)
    fmtx (font metrics)
    fond (font family compatibility)
    fpgm (font program)
    fvar (font variation)
    gasp (grid-fitting and scan-conversion procedure)
    glyf (glyph outline)
    gvar (glyph variation)
    hdmx (horizontal device metrics)
    just (justification)
    kern (kerning)
    kerx (extended kerning)
    lcar (ligature caret)
    loca (glyph location)
    ltag (language tag)
    meta (metadata)
    mort (metamorphosis) table (deprecated)
    morx (extended metamorphosis)
    opbd (optical bounds)
    post (glyph name and PostScript compatibility)
    prep (control value program)
    prop (properties)
    sbix (extended bitmaps)
    trak (tracking)
    vhea (vertical header)
    vmtx (vertical metrics)
    xref (cross-reference)
    Zapf (glyph reference)
"""
