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


# TODO: acnt - Unsure if these are correct table types
@table
class acnt:
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
    majorVersion: uint16
    minorVersion: uint16
    reserved: uint16
    axisCount: uint16
    segmentMaps: tuple[SegmentMaps, ...]


@table
class BASE: ...  # TODO: BASE


@table
class bdat: ...  # TODO: bdat


@table
class bhed: ...  # TODO: bhed


@table
class bloc: ...  # TODO: bloc


@table
class bsln: ...  # TODO: bsln


@table
class CBDT: ...  # TODO: CBDT


@table
class CBLC: ...  # TODO: CBLC


@table
class CFF: ...  # TODO: CFF


@table
class CFF2: ...  # TODO: CFF2


@table
class cmap: ...  # TODO: cmap


@table
class COLR: ...  # TODO: COLR


@table
class CPAL: ...  # TODO: CPAL


@table
class cvar: ...  # TODO: cvar


@table
class cvt:
    program: tuple[FWORD]


@table
class DSIG: ...  # TODO: DSIG


@table
class EBDT: ...  # TODO: EBDT


@table
class EBLC: ...  # TODO: EBLC


@table
class EBSC: ...  # TODO: EBSC


@table
class fdsc: ...  # TODO: fdsc


@table
class feat: ...  # TODO: feat


@table
class fmtx: ...  # TODO: fmtx


@table
class fond: ...  # TODO: fond


@table
class fpgm:
    program: tuple[uint8, ...]


@table
class fvar: ...  # TODO: fvar


@table
class gaspRange:
    rangeMaxPPEM: uint16
    rangeGaspBehavior: uint16


@table
class gasp:
    version: uint16
    numRanges: uint16
    gaspRanges: tuple[gaspRange, ...]


@table
class GDEF: ...  # TODO: GDEF


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
    glyphs: tuple[glyfGlyph, ...]


@table
class GPOS: ...  # TODO: GPOS


@table
class GSUB: ...  # TODO: GSUB


@table
class gvar: ...  # TODO: gvar


@table
class hdmx: ...  # TODO: hdmx


@table
class head:
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
    hMetrics: tuple[LongHorMetric, ...]
    leftSideBearings: tuple[FWORD, ...]


@table
class HVAR: ...  # TODO: HVAR


@table
class JSTF: ...  # TODO: JSTF


@table
class just: ...  # TODO: just


@table
class kern: ...  # TODO: kern


@table
class kerx: ...  # TODO: kerx


@table
class lcar: ...  # TODO: lcar


@table
class loca:
    offsets: tuple[offset16 | offset32, ...]


@table
class ltag: ...  # TODO: ltag


@table
class LTSH: ...  # TODO: LTSH


@table
class MATH: ...  # TODO: MATH


@table
class maxp_v05:
    version: version16dot16
    numGlyphs: uint16


@table
class maxp_v10:
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
class MERG: ...  # TODO: MERG


@table
class meta: ...  # TODO: meta


@table
class mort: ...  # TODO: mort


@table
class morx: ...  # TODO: morx


@table
class MVAR: ...  # TODO: MVAR


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
    version: uint16
    count: uint16
    storageOffset: offset16
    nameRecords: tuple[NameRecord, ...]
    langTagCount: uint16
    langTagRecords: tuple[LangTagRecord, ...]


type name = name_v0 | name_v1


@table
class opbd: ...  # TODO: opbd


@table
class OS2_v0:
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
    panose: tuple[int8, int8, int8, int8, int8, int8, int8, int8, int8, int8]
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
    ulCodePageRange1: uint32
    ulCodePageRange2: uint32


@table
class OS2_v2(OS2_v1):
    sxHeight: FWORD
    sCapHeight: FWORD
    usDefaultChar: uint16
    usBreakChar: uint16
    usMaxContext: uint16


OS2_v3 = OS2_v2
OS2_v4 = OS2_v2


@table
class OS2_v5(OS2_v2):
    usLowerOpticalPointSize: uint16
    usUpperOpticalPointSize: uint16


type OS2 = OS2_v0 | OS2_v1 | OS2_v2 | OS2_v3 | OS2_v4 | OS2_v4


@table
class PCLT:  # TODO: PCLT unique types and functions for fetching them.
    majorVersion: uint16
    minorVersion: uint16
    fontNumber: uint32
    pitch: uint16
    xHeight: uint16
    style: uint16
    typeFamily: uint16
    capHeight: uint16
    symbolSet: uint16
    typeface: tuple[int8, ...]  # Always 16 items
    characterComplement: tuple[int8, ...]  # Always 8 items
    fileName: tuple[int8, ...]  # Always 6 itms
    strokeWeight: int8
    widthType: int8
    serifStyle: uint8
    reserved: uint8


@table
class post_v1:
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
    numGlyphs: uint16
    glyphNameIndex: tuple[uint16, ...]
    stringData: tuple[str, ...]


@table
class post_v25(post_v1):
    numGlyphs: uint16
    offset: tuple[int8, ...]


post_v3 = post_v1
post_v4 = post_v1

type post = post_v1 | post_v2 | post_v25 | post_v3 | post_v4


@table
class prep:
    program: tuple[uint8, ...]


@table
class prop: ...  # TODO: prop


@table
class STAT: ...  # TODO: STAT


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
    header: sbixHeader
    strikes: tuple[Strike, ...]
    glyphs: tuple[sbixGlyph, ...]


@table
class trak: ...  # TODO: trak


@table
class VDMX: ...  # TODO: VDMX


@table
class vhea: ...  # TODO: vhea


@table
class vmtx: ...  # TODO: vmtx


@table
class VORG: ...  # TODO: VORG


@table
class VVAR: ...  # TODO: VVAR


@table
class xref: ...  # TODO: xref


@table
class Zapf: ...  # TODO: Zapf


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

__all__ = (
    "Table",
    "TTCHeader",
    "TTCHeader_v1",
    "TTCHeader_v2",
    "TableDirectory",
    "TableRecord",
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
    "head",
    "hhea",
    "hmtx",
    "maxp",
    "maxp_v05",
    "maxp_v10",
    "name",
    "name_v0",
    "name_v1",
    "OS2",
    "OS2_v1",
    "OS2_v2",
    "OS2_v3",
    "OS2_v4",
    "OS2_v5",
    "post",
    "post_v2",
    "post_v25",
    "cvt",
    "fpgm",
    "prep",
    "gaspRange",
    "gasp",
    "glyf",
    "glyfGlyph",
    "SimpleGlyph",
    "CompositeGlyphDescription",
    "CompositeGlyph",
    "SVG",
    "SVGDocumentRecord",
    "SVGDocumentList",
    "sbix",
    "sbixHeader",
    "Strike",
    "sbixGlyph",
)
