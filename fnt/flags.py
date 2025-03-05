"""
defintiions of all Flags and Enums found in tables
"""

from fnt.types import uint8, uint16, int16, uint32


class sfntVersion:
    TRUE: uint32 = uint32(b"true")  # iOS and OS X only
    V1: uint32 = uint32(b"\x00\x01\x00\x00")
    TYP1: uint32 = uint32(b"typ1")  # iOS and OS X only
    OTTO: uint32 = uint32(b"OTTO")


class Platform:
    UNICODE = uint16(b"\x00\x00")
    MACINTOSH = uint16(b"\x00\x01")
    ISO = uint16(b"\x00\x02")  # deprecated
    WINDOWS = uint16(b"\x00\x03")
    CUSTOM = uint16(b"\x00\x04")


class UnicodeEncoding:
    UNICODE10 = uint16(b"\x00\x00")  # V 1.0 - deprecated
    UNICODE11 = uint16(b"\x00\x01")  # V 1.1 - deprecated
    ISO_IEC = uint16(b"\x00\x02")  # 10646 - deprecated
    UNICODE2_BMP = uint16(b"\x00\x03")  # Unicode BMP only
    UNICODE2_FULL = uint16(b"\x00\x04")  # Unicode Full Repitore
    UNICODE_VAR = uint16(b"\x00\x05")  # Variation Sequences - For format 14
    UNICODE_FULL = uint16(b"\x00\x06")  # Full repitore - For format 13


class MacintoshEncoding:
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


class ISOEncoding:
    ASCII = uint16(b"\x00\x00")  # 7-bit ASCII
    ISO_10646 = uint16(b"\x00\x01")  # ISO 10646
    ISO_8859_1 = uint16(b"\x00\x02")  # ISO 8859-1


class WindowsEncoding:
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
    MIXED = int16.byte(0)
    LEFT_TO_RIGHT = int16.byte(1, signed=True)
    LEFT_TO_RIGHT_NEUTRALS = int16.byte(2)
    RIGHT_TO_LEFT = int16.byte(-1, signed=True)
    RIGHT_TO_LEFT_NEUTRALS = int16.byte(-2, signed=True)


class SimpleGlyphFlags:
    ON_CURVE_POINT = uint8.byte(0x01)
    X_SHORT_VECTOR = uint8.byte(0x02)
    Y_SHORT_VECTOR = uint8.byte(0x04)
    REPEAT_FLAG = uint8.byte(0x08)
    X_IS_SAME_OR_POSITIVE_X_SHORT_VECTOR = uint8.byte(0x10)
    Y_IS_SAME_OR_POSITIVE_Y_SHORT_VECTOR = uint8.byte(0x20)
    OVERLAP_SIMPLE = uint8.byte(0x40)
    Reserved = uint8.byte(0x80)
