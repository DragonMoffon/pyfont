"""
defintiions of all Flags and Enums found in tables
"""

from fnt.types import (
    uint8,
    uint16,
    int16,
    uint32,
    uint32_from_bytes,
)


class sfntVersion:
    TRUE: uint32 = uint32_from_bytes(b"true")  # iOS and OS X only
    V1: uint32 = uint32_from_bytes(b"\x00\x01\x00\x00")
    TYP1: uint32 = uint32_from_bytes(b"typ1")  # iOS and OS X only
    OTTO: uint32 = uint32_from_bytes(b"OTTO")


class Platform:
    UNICODE: uint16 = 0
    MACINTOSH: uint16 = 1
    ISO: uint16 = 2  # deprecated
    WINDOWS: uint16 = 3
    CUSTOM: uint16 = 4


class UnicodeEncoding:
    UNICODE10: uint16 = 0  # V 1.0 - deprecated
    UNICODE11: uint16 = 1  # V 1.1 - deprecated
    ISO_IEC: uint16 = 2  # 10646 - deprecated
    UNICODE2_BMP: uint16 = 3  # Unicode BMP only
    UNICODE2_FULL: uint16 = 4  # Unicode Full Repitore
    UNICODE_VAR: uint16 = 5  # Variation Sequences - For format 14
    UNICODE_FULL: uint16 = 6  # Full repitore - For format 13


class MacintoshEncoding:
    ROMAN: uint16 = 0
    JAPANESE: uint16 = 1
    CHINESE_TRADITIONAL: uint16 = 2
    KOREAN: uint16 = 3
    ARABIC: uint16 = 4
    HEBREW: uint16 = 5
    GREEK: uint16 = 6
    RUSSIAN: uint16 = 7
    RSYMBOL: uint16 = 8
    DEVANAGARI: uint16 = 9
    GURMUKHI: uint16 = 10
    GUJARATI: uint16 = 11
    ODIA: uint16 = 12
    BANGLA: uint16 = 13
    TAMIL: uint16 = 14
    TELUGU: uint16 = 15
    KANNADA: uint16 = 16
    MALAYALAM: uint16 = 17
    SINHALESE: uint16 = 18
    BURMESE: uint16 = 19
    KHMER: uint16 = 20
    THAI: uint16 = 21
    LAOTIAN: uint16 = 22
    GEORGIAN: uint16 = 23
    ARMENIAN: uint16 = 24
    CHINESE_SIMPLIFIED: uint16 = 25
    TIBETAN: uint16 = 26
    MONGOLIAN: uint16 = 27
    GEEZ: uint16 = 28
    SLAVIC: uint16 = 29
    VIETNAMESE: uint16 = 30
    SINDHI: uint16 = 31
    UNINTERPRETED: uint16 = 32


class ISOEncoding:
    ASCII: uint16 = 0  # 7-bit ASCII
    ISO_10646: uint16 = 1  # ISO 10646
    ISO_8859_1: uint16 = 2  # ISO 8859-1


class WindowsEncoding:
    SYMBOL: uint16 = 0
    UNICODE_BMP: uint16 = 0
    SHIFTJIS: uint16 = 0
    PRC: uint16 = 0
    BIG5: uint16 = 0
    WANSUNG: uint16 = 0
    JOHAB: uint16 = 0
    RESERVED0: uint16 = 0
    RESERVED1: uint16 = 0
    RESERVED2: uint16 = 0
    UNICODE_FULL: uint16 = 0


# Custom supports any from 0-255 see:
# https://learn.microsoft.com/en-us/typography/opentype/spec/cmap#custom-platform-platform-id--4-and-otf-windows-nt-compatibility-mapping


# https://learn.microsoft.com/en-us/typography/opentype/spec/head
class headFlags:
    BASELINE0 = 0b0000_0000_0000_0001
    LEFT0 = 0b0000_0000_0000_0010
    POINT_SIZE = 0b0000_0000_0000_0100
    PPEM_INT = 0b0000_0000_0000_1000
    ALTER_WIDTH = 0b0000_0000_0001_0000
    RESERVED = 0b1000_0111_1110_0000  # TODO: Check Apple docs
    LOSSLESS = 0b0000_1000_0000_0000
    CONVERTED = 0b0001_0000_0001_0000
    CLEAR_TYPE = 0b0010_0000_0001_0000
    LAST_RESORT = 0b0100_0000_0001_0000


class macStyle:
    BOLD = 0b0000_0000_0000_0001
    ITALIC = 0b0000_0000_0000_0010
    UNDERLINE = 0b0000_0000_0000_0100
    OUTLINE = 0b0000_0000_0000_1000
    SHADOW = 0b0000_0000_0001_0000
    CONDENSED = 0b0000_0000_0010_0000
    EXTENDED = 0b0000_0000_0100_0000
    RESERVED = 0b1111_1111_1000_0000


class fontDirectionHint:
    MIXED: int16 = 0
    LEFT_TO_RIGHT: int16 = 1
    LEFT_TO_RIGHT_NEUTRALS: int16 = 2
    RIGHT_TO_LEFT: int16 = -1
    RIGHT_TO_LEFT_NEUTRALS: int16 = -2


class SimpleGlyphFlags:
    ON_CURVE_POINT: uint8 = 0x01
    X_SHORT_VECTOR: uint8 = 0x02
    Y_SHORT_VECTOR: uint8 = 0x04
    REPEAT_FLAG: uint8 = 0x08
    X_IS_SAME_OR_POSITIVE_X_SHORT_VECTOR: uint8 = 0x10
    Y_IS_SAME_OR_POSITIVE_Y_SHORT_VECTOR: uint8 = 0x20
    OVERLAP_SIMPLE: uint8 = 0x40
    Reserved: uint8 = 0x80


class CompositeGlyphFlags:
    ARG_1_AND_2_ARE_WORDS: uint16 = 0x0001
    ARGS_ARE_XY_VALUES: uint16 = 0x0002
    ROUND_XY_TO_GRID: uint16 = 0x0004
    WE_HAVE_A_SCALE: uint16 = 0x0008
    MORE_COMPONENTS: uint16 = 0x0020
    WE_HAVE_AN_X_AND_Y_SCALE: uint16 = 0x0040
    WE_HAVE_A_TWO_BY_TWO: uint16 = 0x0080
    WE_HAVE_INSTRUCTIONS: uint16 = 0x0100
    USE_MY_METRICS: uint16 = 0x0200
    OVERLAP_COMPOUND: uint16 = 0x0400
    SCALED_COMPONENT_OFFSET: uint16 = 0x0800
    UNSCALED_COMPONENT_OFFSET: uint16 = 0x1000
    Reserved: uint16 = 0xE010


class GaspFlags:
    GASP_GRIDFIT: uint16 = 0x0001
    GASP_DOGRAY: uint16 = 0x0002
    GASP_SYMMETRIC_GRIDFIT: uint16 = 0x0004
    GASP_SYMMETRIC_SMOOTHING: uint16 = 0x0008
    Reserved: uint16 = 0xFFF0
