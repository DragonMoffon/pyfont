from pathlib import Path

from .font import Font, TableRef
from .tables import (
    Table,
    TableDirectory,
    TableRecord,
    acnt as acntTable,
    ankr as ankrTable,
    avar as avarTable,
    BASE as BASETable,
    bdat as bdatTable,
    bhed as bhedTable,
    bloc as blocTable,
    bsln as bslnTable,
    CBDT as CBDTTable,
    CBLC as CBLCTable,
    CFF as CFFTable,
    CFF2 as CFF2Table,
    cmap as cmapTable,
    COLR as COLRTable,
    CPAL as CPALTable,
    cvar as cvarTable,
    cvt as cvtTable,
    DSIG as DSIGTable,
    EBDT as EBDTTable,
    EBLC as EBLCTable,
    EBSC as EBSCTable,
    fdsc as fdscTable,
    feat as featTable,
    fmtx as fmtxTable,
    fond as fondTable,
    fpgm as fpgmTable,
    fvar as fvarTable,
    gasp as gaspTable,
    GDEF as GDEFTable,
    glyf as glyfTable,
    GPOS as GPOSTable,
    GSUB as GSUBTable,
    gvar as gvarTable,
    hdmx as hdmxTable,
    head as headTable,
    hhea as hheaTable,
    hmtx as hmtxTable,
    HVAR as HVARTable,
    JSTF as JSTFTable,
    just as justTable,
    kern as kernTable,
    kerx as kerxTable,
    lcar as lcarTable,
    loca as locaTable,
    ltag as ltagTable,
    LTSH as LTSHTable,
    MATH as MATHTable,
    maxp as maxpTable,
    MERG as MERGTable,
    meta as metaTable,
    mort as mortTable,
    morx as morxTable,
    MVAR as MVARTable,
    name as nameTable,
    opbd as opbdTable,
    OS2 as OS2Table,
    PCLT as PCLTTable,
    post as postTable,
    prep as prepTable,
    prop as propTable,
    sbix as sbixTable,
    STAT as STATTable,
    SVG as SVGTable,
    trak as trakTable,
    VDMX as VDMXTable,
    vhea as vheaTable,
    vmtx as vmtxTable,
    VORG as VORGTable,
    VVAR as VVARTable,
    xref as xrefTable,
    Zapf as ZapfTable,
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
            raise KeyError(f"font does not contain the {name} table.")

        return self._records[name]

    def get_table_names(self) -> tuple[str, ...]:
        return tuple(self._records.keys())

    def get_tables(self) -> tuple[Table, ...]:
        return tuple(self._tables.values())

    def get_table(self, name: str) -> Table | None:
        if name in self._tables:
            return self._tables[name]

        if name not in self._records:
            raise KeyError(f"font does not contain the {name} table.")

        record = self._records[name]
        table = parsers[name](self, record)
        if table is None:
            raise ValueError(f"Failed to parse {name} table.")
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
    acnt: acntTable | None = TableRef(acntTable)
    ankr: ankrTable | None = TableRef(ankrTable)
    avar: avarTable | None = TableRef(avarTable)
    BASE: BASETable | None = TableRef(BASETable)
    bdat: bdatTable | None = TableRef(bdatTable)
    bhed: bhedTable | None = TableRef(bhedTable)
    bloc: blocTable | None = TableRef(blocTable)
    bsln: bslnTable | None = TableRef(bslnTable)
    CBDT: CBDTTable | None = TableRef(CBDTTable)
    CBLC: CBLCTable | None = TableRef(CBLCTable)
    CFF: CFFTable | None = TableRef(CFFTable, "CFF ")
    CFF2: CFF2Table | None = TableRef(CFF2Table)
    cmap: cmapTable | None = TableRef(cmapTable)
    COLR: COLRTable | None = TableRef(COLRTable)
    CPAL: CPALTable | None = TableRef(CPALTable)
    cvar: cvarTable | None = TableRef(cvarTable)
    cvt: cvtTable | None = TableRef(cvtTable, "cvt ")
    DSIG: DSIGTable | None = TableRef(DSIGTable)
    EBDT: EBDTTable | None = TableRef(EBDTTable)
    EBLC: EBLCTable | None = TableRef(EBLCTable)
    EBSC: EBSCTable | None = TableRef(EBSCTable)
    fdsc: fdscTable | None = TableRef(fdscTable)
    feat: featTable | None = TableRef(featTable)
    fmtx: fmtxTable | None = TableRef(fmtxTable)
    fond: fondTable | None = TableRef(fondTable)
    fpgm: fpgmTable | None = TableRef(fpgmTable)
    fvar: fvarTable | None = TableRef(fvarTable)
    gasp: gaspTable | None = TableRef(gaspTable)
    GDEF: GDEFTable | None = TableRef(GDEFTable)
    glyf: glyfTable | None = TableRef(glyfTable)
    GPOS: GPOSTable | None = TableRef(GPOSTable)
    GSUB: GSUBTable | None = TableRef(GSUBTable)
    gvar: gvarTable | None = TableRef(gvarTable)
    hdmx: hdmxTable | None = TableRef(hdmxTable)
    head: headTable | None = TableRef(headTable)
    hhea: hheaTable | None = TableRef(hheaTable)
    hmtx: hmtxTable | None = TableRef(hmtxTable)
    HVAR: HVARTable | None = TableRef(HVARTable)
    JSTF: JSTFTable | None = TableRef(JSTFTable)
    just: justTable | None = TableRef(justTable)
    kern: kernTable | None = TableRef(kernTable)
    kerx: kerxTable | None = TableRef(kerxTable)
    lcar: lcarTable | None = TableRef(lcarTable)
    loca: locaTable | None = TableRef(locaTable)
    ltag: ltagTable | None = TableRef(ltagTable)
    LTSH: LTSHTable | None = TableRef(LTSHTable)
    MATH: MATHTable | None = TableRef(MATHTable)
    maxp: maxpTable | None = TableRef(maxpTable)
    MERG: MERGTable | None = TableRef(MERGTable)
    meta: metaTable | None = TableRef(metaTable)
    mort: mortTable | None = TableRef(mortTable)
    morx: morxTable | None = TableRef(morxTable)
    MVAR: MVARTable | None = TableRef(MVARTable)
    name: nameTable | None = TableRef(nameTable)
    opbd: opbdTable | None = TableRef(opbdTable)
    OS2: OS2Table | None = TableRef(OS2Table, "OS/2")
    PCLT: PCLTTable | None = TableRef(PCLTTable)
    post: postTable | None = TableRef(postTable)
    prep: prepTable | None = TableRef(prepTable)
    prop: propTable | None = TableRef(propTable)
    sbix: sbixTable | None = TableRef(sbixTable)
    STAT: STATTable | None = TableRef(STATTable)
    SVG: SVGTable | None = TableRef(SVGTable, "SVG ")
    trak: trakTable | None = TableRef(trakTable)
    VDMX: VDMXTable | None = TableRef(VDMXTable)
    vhea: vheaTable | None = TableRef(vheaTable)
    vmtx: vmtxTable | None = TableRef(vmtxTable)
    VORG: VORGTable | None = TableRef(VORGTable)
    VVAR: VVARTable | None = TableRef(VVARTable)
    xref: xrefTable | None = TableRef(xrefTable)
    Zapf: ZapfTable | None = TableRef(ZapfTable)
