from fnt.types import (
    table,
    uint8,
    int8,
    uint16,
    int16,
    uint32,
    offset16,
    offset32,
    UFWORD,
    FWORD,
    fixed,
    F2DOT14,
    LONGDATETIME,
    tag,
    version16dot16,
    int8x6,
    int8x8,
    int8x10,
    int8x16,
)

# fmt: off
from .BASE import (
    BASE,
    BaseHeader_fmt1,
    BaseHeader_fmt11,
    BaseHeader,
    Axis,
    BaseTagList,
    BaseScriptRecord,
    BaseScriptList,
    BaseLangSys,
    BaseScript,
    BaseValues,
    FeatMinMax,
    MinMax,
    BaseCoord_fmt1,
    BaseCoord_fmt2,
    BaseCoord_fmt3,
    BaseCoord
)

from .cmap import (
    cmap,
    EncodingRecord,
    cmapHeader,
    cmapSubtable,
    cmapSubtable_v0,
    cmapSubHeader,
    cmapSubtable_v2,
    cmapSubtable_v4,
    cmapSubtable_v6,
    cmapSubtable_v10,
    MapGroup,
    cmapSubtable_v8,
    cmapSubtable_v12,
    cmapSubtable_v13,
    VariationSelector,
    UnicodeValueRange,
    DefaultUVS,
    UVSMapping,
    NonDefaultUVS,
    cmapSubtable_v14,
)

from .cff import (
    CFF,
    CFF2,
    VORG
)
# fmt: on

# -- TOP LEVEL TABLES --


@table
class TTCHeader_v1:
    ttcTag: tag
    majorVersion: uint16
    minorVersion: uint16
    numFonts: uint32
    tableDirectoryOffsets: tuple[offset32, ...]


@table
class TTCHeader_v2:
    ttcTag: tag
    majorVersion: uint16
    minorVersion: uint16
    numFonts: uint32
    tableDirectoryOffsets: tuple[offset32, ...]
    dsigTag: tag | None
    dsigLength: uint32 | None
    dsigOffset: uint32 | None


type TTCHeader = TTCHeader_v1 | TTCHeader_v2


@table
class TableRecord:
    tableTag: tag
    checksum: uint32
    offset: offset32
    length: uint32


@table
class TableDirectory:
    sfntVersion: uint32
    numTables: uint16
    searchRange: uint16
    entrySelector: uint16
    rangeShift: uint16
    tableRecords: tuple[TableRecord, ...]


# -- FONT TABLES --


@table
class acnt_desciption_fmt0:
    description: uint8  # actually an uint1
    primaryGlyphIndex: uint16
    primaryAttachmentPoint: uint8
    secondaryInfoIndex: uint8


@table
class acnt_desciption_fmt1:
    description: uint8  # actually an uint1
    primaryGlyphIndex: uint16
    extensionOffset: uint16


@table
class acnt_extension:
    components: uint8  # actually an uint1
    secondaryInfoIndex: tuple[uint8, ...]
    primaryAttachmentPoint: tuple[uint8, ...]


@table
class acnt_secondary_data:
    secondaryGlyphIndex: uint16
    secondaryGlyphAttachmentNumber: uint8


@table
class acnt:  # TODO: acnt - Unsure if these are correct table types
    """Accent Attachments"""

    version: F2DOT14
    firstAccentedGlyphIndex: uint16
    lastAccentedGlyphIndex: uint16
    descriptionOffset: uint32
    extensionOffset: uint32
    secondaryOffset: uint32
    glyphs: tuple[acnt_desciption_fmt0 | acnt_desciption_fmt1, ...]
    ext: tuple[acnt_extension, ...]
    accents: tuple[acnt_secondary_data, ...]


@table
class ankr_glyph:
    numPoints: uint32
    anchorPoints: tuple[uint32, ...]


@table
class ankr:
    """Anchor Points"""

    version: uint16
    flags: uint16
    lookupTableOffset: uint32
    glyphDataTableOffset: uint32
    lookupTable: tuple[offset16, ...]
    glyphDataTable: tuple[ankr_glyph, ...]


@table
class AxisValueMap:
    fromCoordinate: F2DOT14
    toCoordinate: F2DOT14


@table
class SegmentMaps:
    positionalMapCount: uint16
    axisValueMaps: tuple[AxisValueMap, ...]


@table
class avar:
    """Axis Variations"""

    majorVersion: uint16
    minorVersion: uint16
    reserved: uint16
    axisCount: uint16
    segmentMaps: tuple[SegmentMaps, ...]


@table
class bdat:  # TODO: bdat
    """Bitmap Data"""

    ...


@table
class bhed:  # TODO: bhed
    """Bitmap Header"""

    ...


@table
class bloc:  # TODO: bloc
    """Bitmap Location"""

    ...


@table
class bsln:  # TODO: bsln
    """Baseline (Apple)"""

    ...


@table
class CBDT:  # TODO: CBDT
    """Color Bitmap Data"""


@table
class CBLC:  # TODO: CBLC
    """Color Bitmap Location"""

    ...


@table
class COLR:  # TODO: COLR
    """Color Glyph Representation"""

    ...


@table
class CPAL:  # TODO: CPAL
    """Color Lookup Table"""  # ?: I think?

    ...


@table
class cvar:  # TODO: cvar
    """CVT Variations"""

    ...


@table
class cvt:
    """Font Instructions"""

    program: tuple[FWORD]


@table
class SignatureBlock_fmt1:
    reserved1: uint16
    reserved2: uint16
    signatureLength: uint32
    signature: tuple[int8, ...]


type SignatureBlock = SignatureBlock_fmt1


@table
class SignatureRecord:
    format: uint32
    length: uint32
    signatureBlockOffset: offset32


@table
class DSIG:
    """Digital Signatures"""

    version: uint32
    numSignatures: uint16
    flags: uint16
    signatureRecords: tuple[SignatureRecord, ...]
    signatureBlocks: tuple[SignatureBlock, ...]


@table
class EBDT:  # TODO: EBDT
    """Embedded Bitmap Data"""

    ...


@table
class EBLC:  # TODO: EBLC
    """Embedded Bitmap Locations"""

    ...


@table
class EBSC:  # TODO: EBSC
    """Embedded Bitmap Scaling Data"""

    ...


@table
class fdsc:  # TODO: fdsc
    """Font Family Substitution Descriptors"""

    ...


@table
class feat:  # TODO: feat
    """Font Features"""

    ...


@table
class fmtx:  # TODO: fmtx
    """Font Metrics"""

    ...


@table
class fond:  # TODO: fond
    """Font Family Compatiblity"""

    ...


@table
class fpgm:
    """Font Program"""

    program: tuple[uint8, ...]


@table
class fvarHeader:
    majorVersion: uint16  # 1
    minorVersion: uint16  # 0
    axesArrayOffset: offset16
    reserved: uint16  # set to 2
    axisCount: uint16
    axisSize: uint16  # set to 0x0014 (20)
    instanceCount: uint16
    instanceSize: uint16  # either axisCount * sizeof(fixed) + 6 or axisCount * sizeof(fixed) + 4


@table
class VariationAxisRecord:
    axisTag: tag
    minValue: fixed
    defaultValue: fixed
    maxValue: fixed
    flags: uint16  # 0x0001 for hidden 0x0002 -> 0xFFFE are reserved
    axisNameID: uint16


@table
class InstanceRecord:
    subfamilyNameID: uint16
    flags: uint16  # set to 0
    coordinates: tuple[fixed, ...]
    postScriptNameID: uint16 = None  # optional (based on instanceSize) # type: ignore


@table
class fvar:
    """Font Variations"""

    header: fvarHeader
    axes: tuple[VariationAxisRecord, ...]
    instances: tuple[InstanceRecord, ...]


@table
class gaspRange:
    rangeMaxPPEM: uint16
    rangeGaspBehavior: uint16


@table
class gasp:
    """Grayscale Rasterization Techniques"""

    version: uint16
    numRanges: uint16
    gaspRanges: tuple[gaspRange, ...]


@table
class GDEFHeader_v10:
    majorVersion: uint16
    minorVersion: uint16
    glyphClassDefOffset: offset16
    attachListOffset: offset16
    ligCaretListOffset: offset16
    markAttachCaretDefOffset: offset16


@table
class GDEFHeader_v12:
    majorVersion: uint16
    minorVersion: uint16
    glyphClassDefOffset: offset16
    attachListOffset: offset16
    ligCaretListOffset: offset16
    markAttachCaretDefOffset: offset16
    markGlyphSetsDefOffset: offset16


@table
class GDEFHeader_v13:
    majorVersion: uint16
    minorVersion: uint16
    glyphClassDefOffset: offset16
    attachListOffset: offset16
    ligCaretListOffset: offset16
    markAttachCaretDefOffset: offset16
    markGlyphSetsDefOffset: offset16
    itemVarStoreOffset: offset32


GDEFHeader = GDEFHeader_v10 | GDEFHeader_v12 | GDEFHeader_v13


@table
class ClassDef_fmt1:
    format: uint16
    startGlyphID: uint16
    glyphCount: uint16
    classValues: tuple[uint16, ...]


@table
class ClassRange:
    startGlyphID: uint16
    endGlyphID: uint16
    # ! class is a reserved keyword in python so Label was added and is not too spec.
    classLabel: uint16


@table
class ClassDef_fmt2:
    format: uint16
    classRangeCount: uint16
    classRangeRecords: tuple[ClassRange, ...]


ClassDef = ClassDef_fmt1 | ClassDef_fmt2


class GlyphClassDefEnum:
    BASE = 1
    LIGATURE = 2
    MARK = 3
    COMPONENT = 4


@table
class AttachPoint:
    pointCount: uint16
    pointIndices: tuple[uint16, ...]


@table
class AttachmentPointList:
    pass


@table
class GDEF:  # TODO: GDEF
    """Glyph Definitions"""

    header: GDEFHeader
    glyphClassDef: ClassDef | None
    attachList: None
    ligCaretList: None
    markAttachClassDef: ClassDef | None
    markGlyphSetsDef: None
    itemVarStore: None


@table
class SimpleGlyph:
    numberOfContours: int16
    xMin: int16
    xMax: int16
    yMin: int16
    yMax: int16
    endPtsOfContours: tuple[uint16, ...]
    instructionLength: uint16
    instructions: tuple[uint8, ...]
    flags: tuple[uint8, ...]
    xCoordinates: tuple[uint8 | int16, ...]
    yCoordinates: tuple[uint8 | int16, ...]


@table
class CompositeGlyphDescription:
    flags: uint16
    glyphIndex: uint16
    xOffset: uint8 | int8 | int16 | uint16
    yOffset: uint8 | int8 | int16 | uint16
    xScale: F2DOT14
    yScale: F2DOT14 = None  # type: ignore
    scale01: F2DOT14 = None  # type: ignore
    scale10: F2DOT14 = None  # type: ignore

    def __post_init__(self):
        if self.yScale is None:
            self.yScale = self.xScale

        if self.scale01 is None or self.scale10 is None:
            self.scale01 = self.scale10 = 1.0

    @property
    def transform(self) -> tuple[float, float, float, float]:
        return self.xScale, self.scale01, self.scale10, self.yScale


@table
class CompositeGlyph:
    numberOfContours: int16
    xMin: int16
    xMax: int16
    yMin: int16
    yMax: int16
    children: tuple[CompositeGlyphDescription, ...]
    instructionLength: uint16
    instructions: tuple[uint8, ...]


type glyfGlyph = SimpleGlyph | CompositeGlyph


@table
class glyf:
    """Glyphs"""

    glyphs: tuple[glyfGlyph, ...]


@table
class GPOS:  # TODO: GPOS
    """Glyph Positioning"""

    ...


@table
class GSUB:  # TODO: GSUB
    """Glyph Substitutions"""


@table
class gvar:  # TODO: gvar
    """Glyph Variations"""

    ...


@table
class hdmx:  # TODO: hdmx
    """Horizontal Device Metrics (Apple)"""

    ...


@table
class head:
    """Header"""

    majorVersion: uint16
    minorVersion: uint16
    fontRevision: fixed
    checksumAdjustment: uint32
    magicNumber: uint32
    flags: uint16
    unitsPerEm: uint16
    created: LONGDATETIME
    modified: LONGDATETIME
    xMin: int16
    yMin: int16
    xMax: int16
    yMax: int16
    macStyle: uint16
    lowestRecPPEM: uint16
    fontDirectionHint: int16
    indexToLocFormat: int16
    glyphDataFormat: int16


@table
class hhea:
    """Horizontal Header"""

    majorVersion: uint16
    minorVersion: uint16
    ascender: FWORD
    decender: FWORD
    lineGap: FWORD
    advanceWidthMax: UFWORD
    minLeftSideBearing: FWORD
    minRightSideBearing: FWORD
    xMaxExtent: FWORD
    caretSlopeRise: int16
    caretSlopeRun: int16
    caretOffset: int16
    RESERVED: tuple[int16, int16, int16, int16]
    metricDataFormat: int16
    numberOfHMetrics: uint16


@table
class LongHorMetric:
    advanceWidth: UFWORD
    lsb: FWORD


@table
class hmtx:
    """Horizontal Metrics"""

    hMetrics: tuple[LongHorMetric, ...]
    leftSideBearings: tuple[FWORD, ...]


@table
class HVAR:  # TODO: HVAR
    """Horizontal Glyph Metrics (Variable Fonts)"""

    ...


@table
class JSTF:  # TODO: JSTF
    """Justification"""

    ...


@table
class just:  # TODO: just
    """Justifitcation"""  # ?: deja vu

    ...


@table
class kern:  # TODO: kern
    """Kerning"""

    ...


@table
class kerx:  # TODO: kerx
    """Kerning (Apple)"""

    ...


@table
class lcar:  # TODO: lcar
    """Ligature Caret (Apple)"""

    ...


@table
class loca:
    """Index-to-location"""

    offsets: tuple[offset16 | offset32, ...]


@table
class ltag:  # TODO: ltag
    """Language Tag (Apple)"""

    ...


@table
class LTSH:  # TODO: LTSH
    """Linear Threshold"""

    ...


@table
class MATH:  # TODO: MATH
    """Mathematical Typesetting"""

    ...


@table
class maxp_v05:
    """Memory Requirements"""

    version: version16dot16
    numGlyphs: uint16


@table
class maxp_v10:
    """Memory Requirements"""

    version: version16dot16
    numGlyphs: uint16
    maxPoints: uint16
    maxContours: uint16
    maxCompositePoints: uint16
    maxCompositeContours: uint16
    maxZones: uint16
    maxTwilightPoints: uint16
    maxStorage: uint16
    maxFunctionDefs: uint16
    maxComponentElements: uint16
    maxComponentDepth: uint16
    maxInstructionDefs: uint16
    maxStackElements: uint16
    maxSizeOfInstructions: uint16


type maxp = maxp_v05 | maxp_v10


@table
class MERG:  # TODO: MERG
    """Merge"""  # ?: what

    ...


@table
class meta:  # TODO: meta
    """Metadata"""

    ...


@table
class mort:  # TODO: mort
    """Glyph Metamorphosis"""  # ?: what??

    ...


@table
class morx:  # TODO: morx
    """Glyph Metamorphosis (Apple)"""  # ?: what (apple)??

    ...


@table
class MVAR:  # TODO: MVAR
    """Metrics Variations"""

    ...


@table
class NameRecord:
    platformID: uint16
    encodingID: uint16
    languageID: uint16
    nameID: uint16
    length: uint16
    stringOffset: offset16
    string: str


@table
class name_v0:
    """Human-readable Names"""

    version: uint16
    count: uint16
    storageOffset: offset16
    nameRecords: tuple[NameRecord, ...]


@table
class LangTagRecord:
    length: uint16
    langTagOffset: offset16
    string: str


@table
class name_v1:
    """Human-readable Names"""

    version: uint16
    count: uint16
    storageOffset: offset16
    nameRecords: tuple[NameRecord, ...]
    langTagCount: uint16
    langTagRecords: tuple[LangTagRecord, ...]


type name = name_v0 | name_v1


@table
class opbd:  # TODO: opbd
    """Optical Bounds"""

    ...


@table
class OS2_v0:
    """Windows-required Metrics"""

    version: uint16
    xAvgCharWidth: FWORD
    usWeightClass: uint16
    usWidthClass: uint16
    fsType: uint16
    ySubscriptXSize: FWORD
    ysubscriptYSize: FWORD
    ySubscriptXOffset: FWORD
    ySubscriptYOffset: FWORD
    ySuperscriptXSize: FWORD
    ySuperscriptYSize: FWORD
    ySuperscriptXOffset: FWORD
    ySuperscriptYOffset: FWORD
    yStrikeoutSize: FWORD
    yStrickoutPosition: FWORD
    sFamilyClass: int16
    panose: int8x10
    ulUnicodeRange1: uint32
    ulUnicodeRange2: uint32
    ulUnicodeRange3: uint32
    ulUnicodeRange4: uint32
    achVendID: tag
    fsSelection: uint16
    usFirstCharIndex: uint16
    usLastCharIndex: uint16
    sTypoAscender: FWORD
    sTypoDescender: FWORD
    sTypeLineGap: FWORD
    usWinAscent: UFWORD
    usWinDescent: UFWORD


@table
class OS2_v1(OS2_v0):
    """Windows-required Metrics"""

    ulCodePageRange1: uint32
    ulCodePageRange2: uint32


@table
class OS2_v2(OS2_v1):
    """Windows-required Metrics"""

    sxHeight: FWORD
    sCapHeight: FWORD
    usDefaultChar: uint16
    usBreakChar: uint16
    usMaxContext: uint16


OS2_v3 = OS2_v2
OS2_v4 = OS2_v2


@table
class OS2_v5(OS2_v2):
    """Windows-required Metrics"""

    usLowerOpticalPointSize: uint16
    usUpperOpticalPointSize: uint16


type OS2 = OS2_v0 | OS2_v1 | OS2_v2 | OS2_v3 | OS2_v4 | OS2_v4


@table
class PCLT:  # TODO: PCLT unique types and functions for fetching them.
    """HP Printer Command Language"""

    majorVersion: uint16
    minorVersion: uint16
    fontNumber: uint32
    pitch: uint16
    xHeight: uint16
    style: uint16
    typeFamily: uint16
    capHeight: uint16
    symbolSet: uint16
    typeface: int8x16  # Always 16 items
    characterComplement: int8x8
    fileName: int8x6
    strokeWeight: int8
    widthType: int8
    serifStyle: uint8
    reserved: uint8


@table
class post_v1:
    """PostScript"""

    version: version16dot16
    italicAngle: fixed
    underlinePosition: FWORD
    uinderlineThickness: FWORD
    isFixedPitch: uint32
    minMemType42: uint32
    maxMemType42: uint32
    minMemType1: uint32
    maxMemType1: uint32


@table
class post_v2(post_v1):
    """PostScript"""

    numGlyphs: uint16
    glyphNameIndex: tuple[uint16, ...]
    stringData: tuple[str, ...]


@table
class post_v25(post_v1):
    """PostScript"""

    numGlyphs: uint16
    offset: tuple[int8, ...]


post_v3 = post_v1
post_v4 = post_v1

type post = post_v1 | post_v2 | post_v25 | post_v3 | post_v4


@table
class prep:
    """CVP Instructions"""

    program: tuple[uint8, ...]


@table
class prop:  # TODO: prop
    """Glyph Properties"""

    ...


@table
class STAT:  # TODO: STAT
    """Style Attributes"""

    ...


@table
class SVGDocumentRecord:
    startGlyphID: uint16
    endGlyphID: uint16
    svgDocOffset: offset32
    svgDocLength: uint32


@table
class SVGDocumentList:
    numEntries: uint16
    documentRecords: tuple[SVGDocumentRecord, ...]


@table
class SVG:
    """Scalable Vector Graphics"""

    version: uint16
    svgDocumentListOffset: offset32
    reserved: uint32
    svgDocumentList: SVGDocumentList


@table
class sbixHeader:
    version: uint16
    flags: uint16
    numStrikes: uint32
    strikeOffsets: tuple[offset32, ...]


@table
class Strike:
    ppem: uint16
    ppi: uint16
    glyphDataOffsets: tuple[offset32, ...]


@table
class sbixGlyph:
    originOffsetX: int16
    originOffsetY: int16
    graphicType: tag
    data: tuple[uint8, ...]


@table
class sbix:
    """Standard Bitmap Graphics"""

    header: sbixHeader
    strikes: tuple[Strike, ...]
    glyphs: tuple[sbixGlyph, ...]


@table
class trak:  # TODO: trak
    """Tracking"""

    ...


@table
class VDMX:  # TODO: VDMX
    """Vertical Device Metrics"""

    ...


@table
class vhea:  # TODO: vhea
    """Vertical Header"""

    ...


@table
class vmtx:  # TODO: vmtx
    """Vertical Metrics"""

    ...


@table
class VVAR:  # TODO: VVAR
    """Vertical Metrics Variations"""


@table
class xref:
    """
    Cross-Reference Table
    Stores symbolic names that are lost during table generation
    Apple only
    Removed on font publications typically
    """

    ...  # TODO: xref


@table
class Zapf:  # TODO: Zapf
    """
    Information about every glyph in the table
    Named after designer Hermann Zapf
    """

    ...


type Table = (
    TTCHeader
    | TableDirectory
    | acnt
    | ankr
    | avar
    | BASE
    | bdat
    | bhed
    | bloc
    | bsln
    | CBDT
    | CBLC
    | CFF
    | CFF2
    | cmap
    | COLR
    | CPAL
    | cvar
    | cvt
    | DSIG
    | EBDT
    | EBLC
    | EBSC
    | fdsc
    | feat
    | fmtx
    | fond
    | fpgm
    | fvar
    | gasp
    | GDEF
    | glyf
    | GPOS
    | GSUB
    | gvar
    | hdmx
    | head
    | hhea
    | hmtx
    | HVAR
    | JSTF
    | just
    | kern
    | kerx
    | lcar
    | loca
    | ltag
    | LTSH
    | MATH
    | maxp
    | MERG
    | meta
    | mort
    | morx
    | MVAR
    | name
    | opbd
    | OS2
    | PCLT
    | post
    | prep
    | prop
    | sbix
    | STAT
    | SVG
    | trak
    | VDMX
    | vhea
    | vmtx
    | VORG
    | VVAR
    | xref
    | Zapf
)

# fmt: off
__all__ = (
    "Table",
    "TTCHeader",
    "TTCHeader_v1",
    "TTCHeader_v2",
    "TableRecord",
    "acnt",
    "ankr",
    "avar",
    "BASE",
    "BaseHeader_fmt1",
    "BaseHeader_fmt11",
    "BaseHeader",
    "Axis",
    "BaseTagList",
    "BaseScriptRecord",
    "BaseScriptList",
    "BaseLangSys",
    "BaseScript",
    "BaseValues",
    "FeatMinMax",
    "MinMax",
    "BaseCoord_fmt1",
    "BaseCoord_fmt2",
    "BaseCoord_fmt3",
    "BaseCoord",
    "bdat",
    "bhed",
    "bloc",
    "bsln",
    "CBDT",
    "CBLC",
    "CFF",
    "CFF2",
    "cmap",
    "EncodingRecord",
    "cmapHeader",
    "cmapSubtable",
    "cmapSubHeader",
    "cmapSubtable_v0",
    "cmapSubtable_v2",
    "cmapSubtable_v4",
    "cmapSubtable_v6",
    "cmapSubtable_v10",
    "MapGroup",
    "cmapSubtable_v8",
    "cmapSubtable_v12",
    "cmapSubtable_v13",
    "VariationSelector",
    "UnicodeValueRange",
    "DefaultUVS",
    "UVSMapping",
    "NonDefaultUVS",
    "cmapSubtable_v14",
    "COLR",
    "CPAL",
    "cvar",
    "cvt",
    "DSIG",
    "EBDT",
    "EBLC",
    "EBSC",
    "fdsc",
    "feat",
    "fmtx",
    "fond",
    "fpgm",
    "fvar",
    "fvarHeader",
    "VariationAxisRecord",
    "InstanceRecord",
    "gasp",
    "gaspRange",
    "GDEF",
    "glyf",
    "glyfGlyph",
    "SimpleGlyph",
    "CompositeGlyphDescription",
    "CompositeGlyph",
    "GPOS",
    "GSUB",
    "gvar",
    "hdmx",
    "head",
    "hhea",
    "hmtx",
    "HVAR",
    "JSTF",
    "just",
    "kern",
    "kerx",
    "lcar",
    "loca",
    "ltag",
    "LTSH",
    "MATH",
    "maxp",
    "maxp_v05",
    "maxp_v10",
    "MERG",
    "meta",
    "mort",
    "morx",
    "MVAR",
    "name",
    "name_v0",
    "name_v1",
    "opbd",
    "OS2",
    "OS2_v1",
    "OS2_v2",
    "OS2_v3",
    "OS2_v4",
    "OS2_v5",
    "PCLT",
    "post",
    "post_v2",
    "post_v25",
    "prep",
    "prop",
    "sbix",
    "sbixHeader",
    "Strike",
    "sbixGlyph",
    "STAT",
    "SVG",
    "SVGDocumentRecord",
    "SVGDocumentList",
    "trak",
    "VDMX",
    "vhea",
    "vmtx",
    "VORG",
    "VVAR",
    "xref",
    "Zapf",
)
# fmt: on
