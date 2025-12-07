from dataclasses import dataclass
from typing import Literal

YES = "✅"
NO = "❌"
APPLE_ICON = "🍎"
CUSTOM_ICON = "🆕"

Format = Literal["ttf", "otf"]

@dataclass
class FontTable:
    id: str
    name: str
    formats: list[Format]
    _description: str = ""
    required_ttf: bool = False
    required_otf: bool = False
    apple_only: bool = False
    deprecated: bool = False
    custom: bool = False
    custom_provider: str | None = None
    defined: bool = False
    parsable: bool = False
    _python_name: str | None = None

    @property
    def python_name(self) -> str:
        return self._python_name or self.id
    
    @property
    def description(self) -> str:
        desc = ""
        desc += f"{self.name}{' ' + APPLE_ICON if self.apple_only else ''}{' ' + CUSTOM_ICON if self.custom else ''}"
        if self._description:
            desc += f"\n{self._description}"
        if self.deprecated:
            desc += " [bold red]DEPRECATED[/bold red]"
        desc += "\nUsed in formats: " + ", ".join([f.upper() for f in self.formats])
        if self.required_ttf and self.required_otf:
            desc += "\n[italic]Required by TTF and OTF.[/italic]"
        elif self.required_ttf:
            desc += "\n[italic]Required by TTF.[/italic]"
        elif self.required_otf:
            desc += "\n[italic]Required by OTF.[/italic]"
        elif self.custom_provider:
            desc += f"\n[italic]Provided by {self.custom_provider}.[/italic]"
        desc += f"\n{YES if self.defined else NO} Defined {YES if self.parsable else NO} Parsable"
        
        return desc

TABLES = [
    FontTable("acnt", "Accent Attachment Table", ["ttf"], deprecated = True),
    FontTable("ankr", "Anchor Point", ["ttf"], "For use with the [u]kerx[/u] table.", apple_only = True, defined = True),
    FontTable("avar", "Axis Variations", ["ttf", "otf"], "Used in variable fonts.", defined = True, parsable = True),
    FontTable("BASE", "Baseline", ["otf"], "Used to align glyphs of different scripts and sizes in a line of text."),
    FontTable("bdat", "Bitmap Data", ["ttf"], "Used in bitmap fonts."),
    FontTable("bhed", "Bitmap Header", ["ttf"], "Used in bitmap fonts."),
    FontTable("bloc", "Bitmap Location", ["ttf"], "Used in bitmap fonts."),
    FontTable("bsln", "Baseline", ["ttf"], "Used to align glyphs of different scripts and sizes in a line of text.", apple_only = True),
    FontTable("CBDT", "Color Bitmap Data", ["otf"], "Used in bitmap fonts."),
    FontTable("CBLC", "Color Bitmap Header", ["otf"], "Used in bitmap fonts."),
    FontTable("CFF ", "Compact Font Format Representation (Version 1)", ["otf"], "In accordance with Adobe Technical Notes #5176 and #5177.", deprecated = True, _python_name = "CFF"),
    FontTable("CFF2", "Compact Font Format Representation (Version 2)", ["otf"], "An alternative to the [u]glyf[/u] table."),
    FontTable("cmap", "Character Map", ["ttf", "otf"], "Defines the mapping of character codes to a default glyph index.", required_ttf = True, required_otf = True, defined = True, parsable = True),
    FontTable("COLR", "Color", ["otf"], "Color presentations for glyphs."),
    FontTable("CPAL", "Color Palette", ["otf"], "Only exists if [u]COLR[/u] is present."),
    FontTable("cvar", "CVT Variations", ["ttf", "otf"], "Variations for the values in the [u]cvt [/u] table."),
    FontTable("cvt ", "Control Value", ["ttf", "otf"], "Contains a list of variables used by instructions.", defined = True, parsable = True),
    FontTable("DSIG", "Digital Signatures", ["otf"], defined = True, parsable = True),
    FontTable("EBDT", "Embedded Bitmap Data", ["otf"]),
    FontTable("EBLC", "Embedded Bitmap Location", ["otf"]),
    FontTable("EBSC", "Embedded Bitmap Scaling", ["ttf", "otf"]),
    FontTable("fdsc", "Font Descriptors", ["ttf"]),
    FontTable("feat", "Feature Name", ["ttf"], apple_only = True),
    FontTable("fmtx", "Font Metrics", ["ttf"]),
    FontTable("fond", "Font Data", ["ttf"], "'Provides the ability to have true data-fork fonts to behave as if they were in a font suitcase with associated FOND data.'", apple_only = True),
    FontTable("fpgm", "Font Program", ["ttf", "otf"], defined = True, parsable = True),
    FontTable("fvar", "Font Variations", ["ttf", "otf"], defined = True, parsable = True),
    FontTable("gasp", "Grid-fitting and Scan-conversion Procedure", ["ttf", "otf"], defined = True),
    FontTable("GDEF", "Glyph Definition", ["otf"]),
    FontTable("glyf", "Glyph Data", ["ttf", "otf"], required_ttf = True, defined = True),
    FontTable("GPOS", "Glyph Positioning", ["otf"]),
    FontTable("GSUB", "Glyph Substitution", ["otf"]),
    FontTable("gvar", "Glyph Variations", ["ttf", "otf"]),
    FontTable("hdmx", "Horizontal Device Metrics", ["ttf", "otf"]),
    FontTable("head", "Font Header", ["ttf", "otf"], required_ttf = True, required_otf = True, defined = True, parsable = True),
    FontTable("hhea", "Horizontal Header", ["ttf", "otf"], required_ttf = True, required_otf = True, defined = True, parsable = True),
    FontTable("hmtx", "Horizontal Metrics", ["ttf", "otf"], required_ttf = True, required_otf = True, defined = True, parsable = True),
    FontTable("HVAR", "Horizontal Metrics Variations", ["otf"]),
    FontTable("JSTF", "Justification", ["otf"]),
    FontTable("just", "Justification", ["ttf"], apple_only = True),
    FontTable("kern", "Kerning", ["ttf", "otf"]),
    FontTable("kerx", "Kerning", ["ttf"], apple_only = True),
    FontTable("lcar", "Ligature Caret", ["ttf"], apple_only = True),
    FontTable("loca", "Glyph Locations", ["ttf", "otf"], defined = True),
    FontTable("ltag", "IETF Language Tags", ["ttf"]),
    FontTable("LTSH", "Linear Threshold", ["otf"]),
    FontTable("MATH", "Mathematical Typesetting", ["otf"]),
    FontTable("maxp", "Maximum Profile", ["ttf", "otf"], "Maximum memory requirements for this font.", required_ttf = True, required_otf = True, defined = True, parsable = True),
    FontTable("MERG", "Merge", ["otf"], "Defines the order of compositing in respect to anti-aliasing."),
    FontTable("meta", "Metadata", ["ttf", "otf"]),
    FontTable("mort", "Glyph Metamorphosis", ["ttf"], apple_only = True, deprecated = True),
    FontTable("morx", "Glyph Metamorphosis", ["ttf"], apple_only = True),
    FontTable("MVAR", "Metrics Variations", ["otf"]),
    FontTable("name", "Naming", ["ttf", "otf"], "Multilingual strings relating to this font.", required_ttf = True, required_otf = True, defined = True, parsable = True),
    FontTable("opbd", "Optical Bounds", ["ttf"], apple_only = True),
    FontTable("OS/2", "Metrics and Data", ["ttf", "otf"], "Required by Windows.", required_ttf = True, required_otf = True, _python_name = "OS2", defined = True, parsable = True),
    FontTable("PCLT", "PCL5 Language", ["otf"], "Provides compatibility with the Hewlett-Packard PCL 5 printer language.", defined = True, parsable = True),
    FontTable("post", "PostScript", ["ttf", "otf"], required_ttf = True, required_otf = True, defined = True, parsable = True),
    FontTable("prep", "Control Value Program", ["ttf", "otf"], "Previously the 'pre-program' table.", defined = True),
    FontTable("prop", "Glyph Properties", ["ttf"], apple_only = True),
    FontTable("sbix", "Standard Bitmap Graphics", ["ttf", "otf"], "Allows bitmap data in standard formats like PNG, TIFF, or JPEG.", defined = True),
    FontTable("STAT", "Style Attributes", ["otf"]),
    FontTable("SVG ", "Scalable Vector Graphics", ["otf"], _python_name = "SVG", defined = True),
    FontTable("trak", "Tracking", ["ttf"], apple_only = True),
    FontTable("VDMX", "Vertical Device Metrics", ["otf"]),
    FontTable("vhea", "Vertical Header", ["ttf", "otf"]),
    FontTable("vmtx", "Vertical Metrics", ["ttf", "otf"]),
    FontTable("VORG", "Vertical Origin", ["otf"]),
    FontTable("VVAR", "Vertical Metrics Variations", ["otf"]),
    FontTable("xref", "Cross-Reference", ["ttf"], "Used by Apple font tools [u]ftxdumperfuser[/u] and [u]ftxenhancer[/u], allowing the generation of other tables using symbolic names."),
    FontTable("Zapf", "Individual Glyph Information", ["ttf"], "Named after legendary type designer Hermann Zapf."),
    FontTable("gcid", "Generic Information", ["ttf"]),
    FontTable("hvgl", "HVF (Hierarchical Variation Font) Glyphs", ["ttf"]),
    FontTable("hvpm", "HVF (Hierarchical Variation Font) Part Remapping", ["ttf"])
]

class FontTableDirectory:
    def __init__(self, tables: list[FontTable]):
        self.tables = tables

    def get_table_by_id(self, id: str) -> FontTable |  None:
        return next((t for t in TABLES if t.id == id), None)
    
    def get_all_table_ids(self) -> list[str]:
        return [t.id for t in TABLES]
    
    def get_all_tables_by_format(self, format: Format) -> list[FontTable]:
        return [t for t in TABLES if format in t.formats]
    
    def get_all_tables_by_custom_status(self, custom: bool) -> list[FontTable]:
        return [t for t in TABLES if t.custom is custom]
    
    def get_all_tables_by_defined_status(self, defined: bool) -> list[FontTable]:
        return [t for t in TABLES if t.defined is defined]
    
    def get_all_tables_by_parsable_status(self, parsable: bool) -> list[FontTable]:
        return [t for t in TABLES if t.parsable is parsable]

TABLE_DIRECTORY = FontTableDirectory(TABLES)
