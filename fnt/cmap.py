"""
This file defines everything described in:
https://learn.microsoft.com/en-us/typography/opentype/spec/cmap

This was also the table that most of types.py was working around.
Hopefully it was diverse enough to support everything.
"""

# fmt: off

from enum import Enum
from math import log2, floor


from fnt.types import (
    definition,
    uint8,
    uint16,
    int16,
    Offset32,
    Array,
    static,
    array,
    dynamic,
)


class Platform(Enum):
    UNICODE = uint16(b"\x00\x00")
    MACINTOSH = uint16(b"\x00\x01")
    ISO = uint16(b"\x00\x02")  # deprecated
    WINDOWS = uint16(b"\x00\x03")
    CUSTOM = uint16(b"\x00\x04")


class UnicodeEncoding(Enum):
    UNICODE10 = uint16(b"\x00\x00")  # V 1.0 - deprecated
    UNICODE11 = uint16(b"\x00\x01")  # V 1.1 - deprecated
    ISO_IEC = uint16(b"\x00\x02")  # 10646 - deprecated
    UNICODE2_BMP = uint16(b"\x00\x03")  # Unicode BMP only
    UNICODE2_FULL = uint16(b"\x00\x04")  # Unicode Full Repitore
    UNICODE_VAR = uint16(b"\x00\x05")  # Variation Sequences - For format 14
    UNICODE_FULL = uint16(b"\x00\x06")  # Full repitore - For format 13


class MacintoshEncoding(Enum):
    ROMAN = uint16(b"\x00\x00")
    JAPANESE = uint16(b"\x00\x01")
    CHINESE_TRADITIONAL = uint16(b"\x00\x02")
    KOREAN = uint16(b"\x00\x03")
    ARABIC = uint16(b"\x00\x04")
    HEBREW = uint16(b"\x00\x05")
    GREEK = uint16(b"\x00\x06")
    RUSSIAN = uint16(b"\x00\x07")
    RSYMBOL = uint16(b"\x00\x08")
    DEVANAGARI = uint16(b"\x00\x09")
    GURMUKHI = uint16(b"\x00\x0A")
    GUJARATI = uint16(b"\x00\x0B")
    ODIA = uint16(b"\x00\x0C")
    BANGLA = uint16(b"\x00\x0D")
    TAMIL = uint16(b"\x00\x0E")
    TELUGU = uint16(b"\x00\x0F")
    KANNADA = uint16(b"\x00\x10")
    MALAYALAM = uint16(b"\x00\x11")
    SINHALESE = uint16(b"\x00\x12")
    BURMESE = uint16(b"\x00\x13")
    KHMER = uint16(b"\x00\x14")
    THAI = uint16(b"\x00\x15")
    LAOTIAN = uint16(b"\x00\x16")
    GEORGIAN = uint16(b"\x00\x17")
    ARMENIAN = uint16(b"\x00\x18")
    CHINESE_SIMPLIFIED = uint16(b"\x00\x19")
    TIBETAN = uint16(b"\x00\x1A")
    MONGOLIAN = uint16(b"\x00\x1B")
    GEEZ = uint16(b"\x00\x1C")
    SLAVIC = uint16(b"\x00\x1D")
    VIETNAMESE = uint16(b"\x00\x1E")
    SINDHI = uint16(b"\x00\x1F")
    UNINTERPRETED = uint16(b"\x00\x20")


class ISOEncoding(Enum):
    ASCII = uint16(b"\x00\x00")  # 7-bit ASCII
    ISO_10646 = uint16(b"\x00\x01")  # ISO 10646
    ISO_8859_1 = uint16(b"\x00\x02")  # ISO 8859-1


class WindowsEncoding(Enum):
    SYMBOL = uint16(b"\x00\x00")
    UNICODE_BMP = uint16(b"\x00\x00")
    SHIFTJIS = uint16(b"\x00\x00")
    PRC = uint16(b"\x00\x00")
    BIG5 = uint16(b"\x00\x00")
    WANSUNG = uint16(b"\x00\x00")
    JOHAB = uint16(b"\x00\x00")
    RESERVED0 = uint16(b"\x00\x00")
    RESERVED1 = uint16(b"\x00\x00")
    RESERVED2 = uint16(b"\x00\x00")
    UNICODE_FULL = uint16(b"\x00\x00")


# Custom supports any from 0-255 see:
# https://learn.microsoft.com/en-us/typography/opentype/spec/cmap#custom-platform-platform-id--4-and-otf-windows-nt-compatibility-mapping


@definition
class EncodingRecord:
    platformID: uint16
    encodingID: uint16
    subtableOffset: Offset32


@definition
class cmapHeader:
    version: uint16
    numTables: uint16
    tables: Array[EncodingRecord] = array("numTables")


@definition
class cmapSubHeader:
    firstCode: uint16
    entryCount: uint16
    idDelta: int16
    idRangeOffset: int16


@definition
class cmapSubtable:
    format: uint16  # Only consistent value between tables (is not copied to versions)


@cmapSubtable.version(uint16(b"\x00\x00"))  # i.e. Format 0
class cmapSubtable:
    format: uint16
    length: uint16
    language: uint16
    glyphIdArray: Array[uint8, 256]


def parse_subHeaders(
    keys: Array[uint16, 256], typ: Array[cmapSubHeader], buffer: bytes, offset: int = 0
):
    k_max = max(keys // 8) + 1  # Get the max possible index for the subHeaders
    return typ[k_max].get(buffer, offset)


def parse_fmt2_glyphIdArray(
    subHeaders: Array[cmapSubHeader], typ: Array[uint16], buffer: bytes, offset: int = 0
):
    # Get the max possible index for the glyphID based on the subHeaders
    j_max = max(
        sub_header.firstCode + sub_header.entryCount for sub_header in subHeaders
    )
    return typ[j_max].get(buffer, offset)


@cmapSubtable.version(uint16(b"\x02"))  # i.e. Format 2
class cmapSubtable:
    format: uint16
    length: uint16
    language: uint16
    subHeaderKeys: Array[uint16, 256]
    subHeaders: Array[cmapSubHeader] = dynamic(parse_subHeaders, "subHeaderKeys")
    glyphIdArray: Array[uint16] = dynamic(parse_fmt2_glyphIdArray, "subHeaders")


def parse_fmt4_glpyhIdArray(

):
    pass


@cmapSubtable.version(uint16(b"\x04"))
class cmapSubtable:
    format: uint16
    length: uint16
    language: uint16
    segCountX2: uint16
    segCount: uint16 = dynamic(lambda s, *_: uint16.byte(s//2), "segCountX2", derived=True) # Not part of actual table
    searchRange: uint16 = dynamic(lambda s, *_: uint16.byte(2 * (2 ** (int(log2(s))))), "segCount") # Only safe to truncate for unsigned ints (find largest power of 2 <= s)
    entrySelector: uint16 = dynamic(lambda s, *_: uint16.byte(int(log2(s))), "segCount") # Is defined as log2(searchRange/2) but that is log2(floor(segCount))s
    rangeShift: uint16 = dynamic(lambda s, r, *_: uint16.byte(s - r), "segCountX2", "searchRange")
    endCode: Array[uint16] = array("segCount")
    reservePad: uint16
    startCode: Array[uint16] = array("segCount")
    idDelta: Array[uint16] = array("segCount")
    idRangeOffset: Array[uint16] = array("segCount")
    glyphIdArray: Array[uint16] = dynamic(parse_fmt4_glpyhIdArray, "segCount")
