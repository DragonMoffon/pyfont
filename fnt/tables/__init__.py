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
