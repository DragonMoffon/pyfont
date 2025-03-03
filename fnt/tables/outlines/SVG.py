from fnt.types import Table, uint16, uint32, Offset32, Array, arrayEntry, dynamicEntry

par

# TODO, provide method for retrieving svg string


class SVGDocumentRecord(Table):
    startGlyphID: uint16
    endGlyphID: uint16
    svgDocOffset: Offset32
    svgDocLength: uint32


class SVGDocumentList(Table):
    numEntries: uint16
    documentRecords: Array[SVGDocumentRecord] = arrayEntry("numEntries")


def derive_svgDocumentList(
    svgDocumentListOffset: Offset32,
    typ: SVGDocumentList,
    buffer: bytes,
    offset: int = 0,
    sz: int = 0,
):
    return typ.read(buffer, offset + svgDocumentListOffset)


class SVG(Table):
    version: uint16
    svgDocumentListOffset: Offset32
    reserved: uint32
    svgDocumentList: SVGDocumentList = dynamicEntry(
        derive_svgDocumentList, "svgDocumentListOffset"
    )
