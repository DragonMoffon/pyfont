from fnt.types import (
    definition,
    versionEntry,
    Tag,
    int8,
    uint16,
    int16,
    uint32,
    FWORD,
    UFWORD,
    Array,
)


@definition
class OS2:
    version: uint16 = versionEntry()


@OS2.add_version(uint16.byte(5))
class OS2:
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
    panose: Array[int8, 10]
    ulUnicodeRange1: uint32
    ulUnicodeRange2: uint32
    ulUnicodeRange3: uint32
    ulUnicodeRange4: uint32
    achVendID: Tag
    fsSelection: uint16
    usFirstCharIndex: uint16
    usLastCharIndex: uint16
    sTypoAscender: FWORD
    sTypoDescender: FWORD
    sTypeLineGap: FWORD
    usWinAscent: UFWORD
    usWinDescent: UFWORD
    ulCodePageRange1: uint32
    ulCodePageRange2: uint32
    sxHeight: FWORD
    sCapHeight: FWORD
    usDefaultChar: uint16
    usBreakChar: uint16
    usMaxContext: uint16
    usLowerOpticalPointSize: uint16
    usUpperOpticalPointSize: uint16


@OS2.add_version(uint16.byte(4))
class OS2:
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
    panose: Array[int8, 10]
    ulUnicodeRange1: uint32
    ulUnicodeRange2: uint32
    ulUnicodeRange3: uint32
    ulUnicodeRange4: uint32
    achVendID: Tag
    fsSelection: uint16
    usFirstCharIndex: uint16
    usLastCharIndex: uint16
    sTypoAscender: FWORD
    sTypoDescender: FWORD
    sTypeLineGap: FWORD
    usWinAscent: UFWORD
    usWinDescent: UFWORD
    ulCodePageRange1: uint32
    ulCodePageRange2: uint32
    sxHeight: FWORD
    sCapHeight: FWORD
    usDefaultChar: uint16
    usBreakChar: uint16
    usMaxContext: uint16


@OS2.add_version(uint16.byte(3))
class OS2:
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
    panose: Array[int8, 10]
    ulUnicodeRange1: uint32
    ulUnicodeRange2: uint32
    ulUnicodeRange3: uint32
    ulUnicodeRange4: uint32
    achVendID: Tag
    fsSelection: uint16
    usFirstCharIndex: uint16
    usLastCharIndex: uint16
    sTypoAscender: FWORD
    sTypoDescender: FWORD
    sTypeLineGap: FWORD
    usWinAscent: UFWORD
    usWinDescent: UFWORD
    ulCodePageRange1: uint32
    ulCodePageRange2: uint32
    sxHeight: FWORD
    sCapHeight: FWORD
    usDefaultChar: uint16
    usBreakChar: uint16
    usMaxContext: uint16


@OS2.add_version(uint16.byte(2))
class OS2:
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
    panose: Array[int8, 10]
    ulUnicodeRange1: uint32
    ulUnicodeRange2: uint32
    ulUnicodeRange3: uint32
    ulUnicodeRange4: uint32
    achVendID: Tag
    fsSelection: uint16
    usFirstCharIndex: uint16
    usLastCharIndex: uint16
    sTypoAscender: FWORD
    sTypoDescender: FWORD
    sTypeLineGap: FWORD
    usWinAscent: UFWORD
    usWinDescent: UFWORD
    ulCodePageRange1: uint32
    ulCodePageRange2: uint32
    sxHeight: FWORD
    sCapHeight: FWORD
    usDefaultChar: uint16
    usBreakChar: uint16
    usMaxContext: uint16


@OS2.add_version(uint16.byte(1))
class OS2:
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
    panose: Array[int8, 10]
    ulUnicodeRange1: uint32
    ulUnicodeRange2: uint32
    ulUnicodeRange3: uint32
    ulUnicodeRange4: uint32
    achVendID: Tag
    fsSelection: uint16
    usFirstCharIndex: uint16
    usLastCharIndex: uint16
    sTypoAscender: FWORD
    sTypoDescender: FWORD
    sTypeLineGap: FWORD
    usWinAscent: UFWORD
    usWinDescent: UFWORD
    ulCodePageRange1: uint32
    ulCodePageRange2: uint32


@OS2.add_version(uint16.byte(0))
class OS2:
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
    panose: Array[int8, 10]
    ulUnicodeRange1: uint32
    ulUnicodeRange2: uint32
    ulUnicodeRange3: uint32
    ulUnicodeRange4: uint32
    achVendID: Tag
    fsSelection: uint16
    usFirstCharIndex: uint16
    usLastCharIndex: uint16
    sTypoAscender: FWORD
    sTypoDescender: FWORD
    sTypeLineGap: FWORD
    usWinAscent: UFWORD
    usWinDescent: UFWORD
