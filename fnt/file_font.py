from pathlib import Path

from .font import Font, TableRef
from .tables import (
    Table,
    TableDirectory,
    TableRecord,
    head as headTable,
    hhea as hheaTable,
    hmtx as hmtxTable,
    maxp as maxpTable,
    cmap as cmapTable,
    OS2 as OS2Table,
    post as postTable,
)
from .parsing import parsers, parse_table_directory


# File Fonts hold and manage their own byte data. They can do what the like with it, and
# aren't beholdent to a collection.
class FileFont(Font):
    def __init__(self, data: bytes, src: Path | None = None):
        self._data: bytes = data
        self._src = src

        self._byte_offset: int = 0

        table_directory = parse_table_directory(self, 0)
        self._records: dict[str, TableRecord] = {
            record.tableTag: record for record in table_directory.tableRecords
        }
        self._tables: dict[str, Table] = {"directory": table_directory}

    def seek(self, offset: int):
        self._byte_offset = offset

    def read(self, sz: int) -> bytes:
        n = self._byte_offset + sz
        b = self._data[self._byte_offset : n]
        self._byte_offset = n
        return b

    def pointer(self) -> int:
        return self._byte_offset

    def get_record(self, name: str) -> TableRecord:
        if name not in self._records:
            # TODO: make custom error for this
            raise KeyError(f"font does not contain the table [{name}]")

        return self._records[name]

    def get_table_names(self) -> tuple[str, ...]:
        return tuple(self._records.keys())

    def get_tables(self) -> tuple[Table, ...]:
        return tuple(self._tables.values())

    def get_table(self, name: str) -> Table | None:
        if name in self._tables:
            return self._tables[name]

        if name not in self._records:
            raise KeyError(f"font does not contain the table [{name}]")

        record = self._records[name]
        table = parsers[name](self, record)
        self._tables[record.tableTag] = table

        return table

    def has_table(self, name: str) -> bool:
        return name in self._records or name in self._tables

    def is_table_parsed(self, name: str) -> bool:
        return name in self._tables

    @classmethod
    def from_file(cls, file: Path):
        with open(file, "rb") as fp:
            data = fp.read()
        return cls(data, file)

    # -- TableRefs for better type checking --
    directory: TableDirectory | None = TableRef(TableDirectory, "directory")
    # acnt = TableRef(acnt)
    # ankr = TableRef(ankr)
    # avar = TableRef(avar)
    # BASE = TableRef(BASE)
    # bdat = TableRef(bdat)
    # bhed = TableRef(bhed)
    # bloc = TableRef(bloc)
    # bsln = TableRef(bsln)
    # CBDT = TableRef(CBDT)
    # CBLC = TableRef(CBLC)
    # CFF  = TableRef(CFF, "CFF ")
    # CFF2 = TableRef(CFF2)
    cmap: cmapTable | None = TableRef(cmapTable)
    # COLR = TableRef(COLR)
    # CPAL = TableRef(CPAL)
    # cvar = TableRef(cvar)
    # cvt  = TableRef(cvt, "cvt ")
    # DSIG = TableRef(DSIG)
    # EBDT = TableRef(EBDT)
    # EBLC = TableRef(EBLC)
    # EBSC = TableRef(EBSC)
    # fdsc = TableRef(fdsc)
    # feat = TableRef(feat)
    # fmtx = TableRef(fmtx)
    # fond = TableRef(fond)
    # fpgm = TableRef(fpgm)
    # fvar = TableRef(fvar)
    # gasp = TableRef(gasp)
    # GDEF = TableRef(GDEF)
    # glyf = TableRef(glyf)
    # GPOS = TableRef(GPOS)
    # GSUB = TableRef(GSUB)
    # gvar = TableRef(gvar)
    # hdmx = TableRef(hdmx)
    head: headTable | None = TableRef(headTable)
    hhea: hheaTable | None = TableRef(hheaTable)
    hmtx: hmtxTable | None = TableRef(hmtxTable)
    # HVAR = TableRef(HVAR)
    # JSTF = TableRef(JSTF)
    # just = TableRef(just)
    # kern = TableRef(kern)
    # kerx = TableRef(kerx)
    # lcar = TableRef(lcar)
    # loca = TableRef(loca)
    # ltag = TableRef(ltag)
    # LTSH = TableRef(LTSH)
    # MATH = TableRef(MATH)
    maxp: maxpTable | None = TableRef(maxpTable)
    # MERG = TableRef(MERG)
    # meta = TableRef(meta)
    # mort = TableRef(mort)
    # morx = TableRef(morx)
    # MVAR = TableRef(MVAR)
    # name = TableRef(name)
    # opbd = TableRef(opbd)
    OS2: OS2Table | None = TableRef(OS2Table, "OS/2")
    # PCLT = TableRef(PCLT)
    post: postTable | None = TableRef(postTable)
    # prep = TableRef(prep)
    # prop = TableRef(prop)
    # sbix = TableRef(sbix)
    # STAT = TableRef(STAT)
    # SVG  = TableRef(SVG, "SVG ")
    # trak = TableRef(trak)
    # VDMX = TableRef(VDMX)
    # vhea = TableRef(vhea)
    # vmtx = TableRef(vmtx)
    # VORG = TableRef(VORG)
    # VVAR = TableRef(VVAR)
    # xref = TableRef(xref)
    # Zapf = TableRef(Zapf)
