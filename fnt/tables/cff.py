from fnt.types import table, uint8, uint16, offset8, offset16, offset24, offset32, offset


@table
class CFFIndex:
    count: uint16
    offSize: uint8
    offsets: tuple[offset, ...]
    data: tuple[tuple[uint8, ...], ...]


@table
class CFFStringIndex:
    count: uint16
    offSize: uint8
    offsets: tuple[offset, ...]
    data: tuple[str, ...]


@table
class CFFHeader:
    major: uint8
    minor: uint8
    hdrSize: uint8
    offSize: uint8


@table
class CFFFont:
    CharStringsIndex: CFFIndex
    FontDictIndex: CFFIndex | None
    PrivateDICT = None
    LocalSubrIndex: CFFIndex | None = None


@table
class CFF:  # TODO: CFF
    """Compat Font Format repesentation v1"""

    header: CFFHeader
    nameIndex: CFFStringIndex
    topDICTIndex: CFFIndex
    stringIndex: CFFStringIndex
    GlobalSubrIndex: CFFIndex
    Encodings = None
    Charsets = None
    FDSelect: None = None
    fonts: tuple[CFFFont, ...] = ()
    Notices: str = ""


@table
class CFF2:  # TODO: CFF2
    """Compat Font Format repesentation v2"""

    ...


@table
class VORG:  # TODO: VORG
    """Vertical Origin"""

    ...
