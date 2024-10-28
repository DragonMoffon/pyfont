"""
defintiions of all Flags and Enums found in tables
"""

from fnt.types import uint16, uint32


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
