from math import log2, floor

from fnt.font import Font, ParseMethod
from fnt.tables import (
    TableRecord,
    TableDirectory,
    acnt,
    AxisValueMap,
    SegmentMaps,
    avar,
    ankr,
    BASE,
    bdat,
    bhed,
    bloc,
    bsln,
    CBDT,
    CBLC,
    CFF,
    CFF2,
    cmap,
    cmapHeader,
    EncodingRecord,
    MapGroup,
    VariationSelector,
    UnicodeValueRange,
    DefaultUVS,
    UVSMapping,
    NonDefaultUVS,
    cmapSubtable,
    cmapSubtable_v0,
    cmapSubHeader,
    cmapSubtable_v2,
    cmapSubtable_v4,
    cmapSubtable_v6,
    cmapSubtable_v8,
    cmapSubtable_v10,
    cmapSubtable_v12,
    cmapSubtable_v13,
    cmapSubtable_v14,
    COLR,
    CPAL,
    cvar,
    cvt,
    SignatureBlock_fmt1,
    SignatureBlock,
    SignatureRecord,
    DSIG,
    EBDT,
    EBLC,
    EBSC,
    fdsc,
    feat,
    fmtx,
    fond,
    fpgm,
    fvar,
    gasp,
    GDEF,
    glyf,
    GPOS,
    GSUB,
    gvar,
    hdmx,
    head,
    hhea,
    LongHorMetric,
    hmtx,
    HVAR,
    JSTF,
    just,
    kern,
    kerx,
    lcar,
    loca,
    ltag,
    LTSH,
    MATH,
    maxp,
    maxp_v05,
    maxp_v10,
    MERG,
    meta,
    mort,
    morx,
    MVAR,
    name,
    NameRecord,
    LangTagRecord,
    name_v0,
    name_v1,
    opbd,
    OS2,
    OS2_v0,
    OS2_v1,
    OS2_v5,
    OS2_v4,
    PCLT,
    post,
    post_v1,
    post_v2,
    post_v25,
    prep,
    prop,
    sbix,
    STAT,
    SVG,
    trak,
    VDMX,
    vhea,
    vmtx,
    VORG,
    VVAR,
    xref,
    Zapf,
)
from fnt.flags import Platform, WindowsEncoding, MacintoshEncoding


# -- TOP LEVEL TABLES --

# TODO: Font Collection Header


def parse_table_record(font: Font) -> TableRecord:
    return TableRecord(
        font.get_tag(), font.get_uint32(), font.get_offset32(), font.get_uint32()
    )


def parse_table_directory(font: Font, offset: int = 0) -> TableDirectory:
    font.seek(offset)

    version = font.get_uint32()  # 4 bytes
    num_tables = font.get_int16()  # 2 bytes

    search_range = 16 * 2 ** (floor(log2(num_tables)))  # 2 bytes
    entry_selector = floor(log2(num_tables))  # 2 bytes
    range_shift = num_tables * 16 - search_range  # 2 bytes

    font.seek(offset + 12)  # move 12 bytes to get to correct location
    records = tuple(parse_table_record(font) for _ in range(num_tables))

    return TableDirectory(
        version, num_tables, search_range, entry_selector, range_shift, records
    )


# -- FONT TABLES --


def parse_acnt(font: Font, record: TableRecord) -> acnt: ...  # TODO: acnt
def parse_ankr(font: Font, record: TableRecord) -> ankr: ...  # TODO: ankr


def parse_SegmentMaps(font: Font) -> SegmentMaps:
    count = font.get_uint16()
    return SegmentMaps(
        count,
        tuple(
            AxisValueMap(font.get_F2DOT14(), font.get_F2DOT14()) for _ in range(count)
        ),
    )


def parse_avar(font: Font, record: TableRecord) -> avar:
    font.seek(record.offset)
    major = font.get_uint16()
    minor = font.get_uint16()
    reserved = font.get_uint16()
    count = font.get_uint16()
    return avar(
        major,
        minor,
        reserved,
        count,
        tuple(parse_SegmentMaps(font) for _ in range(count)),
    )


def parse_BASE(font: Font, record: TableRecord) -> BASE: ...  # TODO: BASE
def parse_bdat(font: Font, record: TableRecord) -> bdat: ...  # TODO: bdat
def parse_bhed(font: Font, record: TableRecord) -> bhed: ...  # TODO: bhed
def parse_bloc(font: Font, record: TableRecord) -> bloc: ...  # TODO: bloc
def parse_bsln(font: Font, record: TableRecord) -> bsln: ...  # TODO: bsln
def parse_CBDT(font: Font, record: TableRecord) -> CBDT: ...  # TODO: CBDT
def parse_CBLC(font: Font, record: TableRecord) -> CBLC: ...  # TODO: CBLC
def parse_CFF(font: Font, record: TableRecord) -> CFF: ...  # TODO: CFF
def parse_CFF2(font: Font, record: TableRecord) -> CFF2: ...  # TODO: CFF2


def parse_map_group(font: Font):
    return MapGroup(font.get_uint32(), font.get_uint32(), font.get_uint32())


def parse_variation_selector(font: Font):
    return VariationSelector(
        font.get_uint32(),
        font.get_offset32(),
        font.get_offset32(),
    )


def parse_cmap_subtable(
    font: Font, record: TableRecord, encoding: EncodingRecord
) -> cmapSubtable:
    offset = record.offset + encoding.subtableOffset
    font.seek(offset)
    fmt = font.get_uint16()
    match fmt:
        case 0:
            return cmapSubtable_v0(
                fmt,
                font.get_uint16(),
                font.get_uint16(),
                font.get_uint8_array(256),
            )
        case 2:
            length = font.get_uint16()
            language = font.get_uint16()
            keys = font.get_uint16_array(256)
            sub_headers = tuple(
                cmapSubHeader(
                    font.get_uint16(),
                    font.get_uint16(),
                    font.get_uint16(),
                    font.get_int16(),
                )
                for _ in range(max(keys) // 8 + 1)
            )
            # TODO: Validate this is a safe method of getting length.
            table_remainder = (record.offset + record.length) - font.pointer()
            glyph_id_range = font.get_uint16_array(table_remainder // 2)
            return cmapSubtable_v2(
                fmt,
                length,
                language,
                keys,
                sub_headers,
                glyph_id_range,
            )
        case 4:
            length = font.get_uint16()
            language = font.get_uint16()
            seg_count_x2 = font.get_uint16()
            font.get_uint16_array(3)  # Skip search values and derive.
            search_range = 2 ** int(log2(seg_count_x2))
            entry_selector = int(log2(seg_count_x2 / 2.0))
            range_shift = seg_count_x2 - search_range

            return cmapSubtable_v4(
                fmt,
                length,
                language,
                seg_count_x2,
                search_range,
                entry_selector,
                range_shift,
                font.get_uint16_array(seg_count_x2 // 2),
                font.get_uint16(),
                font.get_uint16_array(seg_count_x2 // 2),
                font.get_uint16_array(seg_count_x2 // 2),
                font.get_uint16_array(seg_count_x2 // 2),
                font.get_uint16_array((offset + length) - font.pointer()),
            )
        case 6:
            length = font.get_uint16()
            return cmapSubtable_v6(
                fmt,
                length,
                font.get_uint16(),
                font.get_uint16(),
                font.get_uint16(),
                font.get_uint16_array(length),
            )
        case 8:
            length = font.get_uint16()
            language = font.get_uint16()
            is32 = font.get_uint8_array(8192)
            count = font.get_uint32()
            return cmapSubtable_v8(
                fmt,
                length,
                language,
                is32,
                count,
                tuple(parse_map_group(font) for _ in range(count)),
            )
        case 10:
            reserved = font.get_uint16()
            length = font.get_uint16()
            return cmapSubtable_v10(
                fmt,
                reserved,
                length,
                font.get_uint32(),
                font.get_uint32(),
                font.get_uint32(),
                font.get_uint16_array(length),
            )
        case 12:
            reserved = font.get_uint16()
            length = font.get_uint32()
            language = font.get_uint32()
            count = font.get_uint32()
            return cmapSubtable_v12(
                fmt,
                reserved,
                length,
                language,
                count,
                tuple(parse_map_group(font) for _ in range(count)),
            )
        case 13:
            reserved = font.get_uint16()
            length = font.get_uint32()
            count = font.get_uint32()
            return cmapSubtable_v13(
                fmt,
                reserved,
                length,
                count,
                tuple(parse_map_group(font) for _ in range(count)),
            )
        case 14:
            length = font.get_uint16()
            count = font.get_uint32()
            selectors = tuple(parse_variation_selector(font) for _ in range(count))
            default = []
            non_default = []
            for selector in selectors:
                if selector.defaultUVSOffset != 0:
                    font.seek(offset + selector.defaultUVSOffset)
                    num = font.get_uint32()
                    ranges = tuple(
                        UnicodeValueRange(font.get_uint24(), font.get_uint8())
                        for _ in range(num)
                    )
                    default.append(DefaultUVS(num, ranges))

                if selector.nonDefaultUVSOffset != 0:
                    font.seek(offset + selector.nonDefaultUVSOffset)
                    num = font.get_uint32()
                    mappings = tuple(
                        UVSMapping(font.get_uint24(), font.get_uint16())
                        for _ in range(num)
                    )
                    non_default.append(NonDefaultUVS(num, mappings))
            return cmapSubtable_v14(
                fmt, length, count, selectors, tuple(default), tuple(non_default)
            )


def parse_cmap(font: Font, record: TableRecord) -> cmap:
    font.seek(record.offset)

    heaader_version = font.get_uint16()
    num_tables = font.get_uint16()
    header = cmapHeader(
        heaader_version,
        num_tables,
        tuple(
            EncodingRecord(font.get_uint16(), font.get_uint16(), font.get_offset32())
            for _ in range(num_tables)
        ),
    )

    sub_table_offsets: dict[int, cmapSubtable] = {}
    sub_tables = []
    for encoding in header.encodingRecords:
        if encoding.subtableOffset in sub_table_offsets:
            sub_tables.append(sub_table_offsets[encoding.subtableOffset])
            continue
        sub_table = parse_cmap_subtable(font, record, encoding)
        sub_tables.append(sub_table)
        sub_table_offsets[encoding.subtableOffset] = sub_table

    return cmap(
        header,
        tuple(
            parse_cmap_subtable(font, record, encoding)
            for encoding in header.encodingRecords
        ),
    )


def parse_COLR(font: Font, record: TableRecord) -> COLR: ...  # TODO: COLR
def parse_CPAL(font: Font, record: TableRecord) -> CPAL: ...  # TODO: CPAL
def parse_cvar(font: Font, record: TableRecord) -> cvar: ...  # TODO: cvar


def parse_cvt(font: Font, record: TableRecord) -> cvt:
    font.seek(record.offset)
    return cvt(tuple(font.get_FWORD_array(record.length // 2)))


def parse_SignatureBlock(
    font: Font, offset: int, record: SignatureRecord
) -> SignatureBlock:
    font.seek(offset + record.signatureBlockOffset)
    if record.format == 1:
        r1, r2 = font.get_uint16(), font.get_uint16()
        length = font.get_uint32()
        signature = font.get_uint8_array(length)
        return SignatureBlock_fmt1(r1, r2, length, signature)
    raise ValueError(f"Invalid Signature Format ({record.format}).")


def parse_DSIG(font: Font, record: TableRecord) -> DSIG:
    font.seek(record.offset)
    version = font.get_uint32()
    count = font.get_uint16()
    flags = font.get_uint16()
    records = tuple(
        SignatureRecord(font.get_uint32(), font.get_uint32(), font.get_offset32())
        for _ in range(count)
    )
    blocks = tuple(
        parse_SignatureBlock(font, record.offset, sig_record) for sig_record in records
    )
    return DSIG(version, count, flags, records, blocks)


def parse_EBDT(font: Font, record: TableRecord) -> EBDT: ...  # TODO: EBDT
def parse_EBLC(font: Font, record: TableRecord) -> EBLC: ...  # TODO: EBLC
def parse_EBSC(font: Font, record: TableRecord) -> EBSC: ...  # TODO: EBSC
def parse_fdsc(font: Font, record: TableRecord) -> fdsc: ...  # TODO: fdsc
def parse_feat(font: Font, record: TableRecord) -> feat: ...  # TODO: feat
def parse_fmtx(font: Font, record: TableRecord) -> fmtx: ...  # TODO: fmtx
def parse_fond(font: Font, record: TableRecord) -> fond: ...  # TODO: fond
def parse_fpgm(font: Font, record: TableRecord) -> fpgm: ...  # TODO: fpgm
def parse_fvar(font: Font, record: TableRecord) -> fvar: ...  # TODO: fvar
def parse_gasp(font: Font, record: TableRecord) -> gasp: ...  # TODO: gasp
def parse_GDEF(font: Font, record: TableRecord) -> GDEF: ...  # TODO: GDEF
def parse_glyf(font: Font, record: TableRecord) -> glyf: ...  # TODO: glyf
def parse_GPOS(font: Font, record: TableRecord) -> GPOS: ...  # TODO: GPOS
def parse_GSUB(font: Font, record: TableRecord) -> GSUB: ...  # TODO: GSUB
def parse_gvar(font: Font, record: TableRecord) -> gvar: ...  # TODO: gvar
def parse_hdmx(font: Font, record: TableRecord) -> hdmx: ...  # TODO: hdmx


def parse_head(font: Font, record: TableRecord) -> head:
    font.seek(record.offset)
    return head(
        font.get_uint16(),
        font.get_uint16(),
        font.get_fixed(),
        font.get_uint32(),
        font.get_uint32(),
        font.get_uint16(),
        font.get_uint16(),
        font.get_time(),
        font.get_time(),
        font.get_int16(),
        font.get_int16(),
        font.get_int16(),
        font.get_int16(),
        font.get_uint16(),
        font.get_uint16(),
        font.get_int16(),
        font.get_int16(),
        font.get_int16(),
    )


def parse_hhea(font: Font, record: TableRecord) -> hhea:
    font.seek(record.offset)
    return hhea(
        font.get_uint16(),
        font.get_uint16(),
        font.get_FWORD(),
        font.get_FWORD(),
        font.get_UFWORD(),
        font.get_FWORD(),
        font.get_FWORD(),
        font.get_FWORD(),
        font.get_FWORD(),
        font.get_int16(),
        font.get_int16(),
        font.get_int16(),
        font.get_int16_array(4),
        font.get_int16(),
        font.get_uint16(),
    )


def parse_hmtx(font: Font, record: TableRecord) -> hmtx:
    num_glpyhs: int = font.get_table("maxp").numGlyphs
    number_of_metrics: int = font.get_table("hhea").numberOfHMetrics

    font.seek(record.offset)

    metrics = tuple(
        LongHorMetric(font.get_UFWORD(), font.get_FWORD())
        for _ in range(number_of_metrics)
    )
    side_beaings = font.get_FWORD_array(num_glpyhs - number_of_metrics)

    return hmtx(metrics, side_beaings)


def parse_HVAR(font: Font, record: TableRecord) -> HVAR: ...  # TODO: HVAR
def parse_JSTF(font: Font, record: TableRecord) -> JSTF: ...  # TODO: JSTF
def parse_just(font: Font, record: TableRecord) -> just: ...  # TODO: just
def parse_kern(font: Font, record: TableRecord) -> kern: ...  # TODO: kern
def parse_kerx(font: Font, record: TableRecord) -> kerx: ...  # TODO: kerx
def parse_lcar(font: Font, record: TableRecord) -> lcar: ...  # TODO: lcar
def parse_loca(font: Font, record: TableRecord) -> loca: ...  # TODO: loca
def parse_ltag(font: Font, record: TableRecord) -> ltag: ...  # TODO: ltag
def parse_LTSH(font: Font, record: TableRecord) -> LTSH: ...  # TODO: LTSH
def parse_MATH(font: Font, record: TableRecord) -> MATH: ...  # TODO: MATH


def parse_maxp(font: Font, record: TableRecord) -> maxp:
    font.seek(record.offset)
    version = font.get_version_legacy()

    if version == 0.5:
        return maxp_v05(version, font.get_uint16())
    return maxp_v10(
        version,
        font.get_uint16(),
        font.get_uint16(),
        font.get_uint16(),
        font.get_uint16(),
        font.get_uint16(),
        font.get_uint16(),
        font.get_uint16(),
        font.get_uint16(),
        font.get_uint16(),
        font.get_uint16(),
        font.get_uint16(),
        font.get_uint16(),
        font.get_uint16(),
        font.get_uint16(),
    )


def parse_MERG(font: Font, record: TableRecord) -> MERG: ...  # TODO: MERG
def parse_meta(font: Font, record: TableRecord) -> meta: ...  # TODO: meta
def parse_mort(font: Font, record: TableRecord) -> mort: ...  # TODO: mort
def parse_morx(font: Font, record: TableRecord) -> morx: ...  # TODO: morx
def parse_MVAR(font: Font, record: TableRecord) -> MVAR: ...  # TODO: MVAR


def parse_name(font: Font, record: TableRecord) -> name:
    font.seek(record.offset)
    version = font.get_uint16()
    count = font.get_uint16()
    offset = font.get_offset16()
    records = tuple(
        NameRecord(
            font.get_uint16(),
            font.get_uint16(),
            font.get_uint16(),
            font.get_uint16(),
            font.get_uint16(),
            font.get_offset16(),
            "",
        )
        for _ in range(count)
    )
    lang_tag_count = 0 if version == 0 else font.get_uint16()
    lang_tags = tuple(
        LangTagRecord(font.get_uint16(), font.get_offset16(), "")
        for _ in range(lang_tag_count)
    )

    data_location = record.offset + offset
    font.seek(record.offset + offset)  # seek to data area for the name string data
    for name_record in records:
        font.seek(data_location + name_record.stringOffset)
        b = font.read(name_record.length)
        encoding = "UTF-16BE"
        match name_record.platformID:
            case Platform.MACINTOSH:
                match name_record.encodingID:
                    case MacintoshEncoding.ROMAN:
                        encoding = "mac-roman"
            case Platform.WINDOWS:
                match name_record.encodingID:
                    case WindowsEncoding.SHIFTJIS:
                        encoding = "936"
                    case WindowsEncoding.BIG5:
                        encoding = "950"
                    case WindowsEncoding.WANSUNG:
                        encoding = "949"
        name_record.string = b.decode(encoding)

    for lang_tag in lang_tags:
        font.seek(data_location + lang_tag.langTagOffset)
        lang_tag.string = font.read(lang_tag.length).decode("UTF-16BE")

    if version == 0:
        return name_v0(version, count, offset, records)
    return name_v1(version, count, offset, records, lang_tag_count, lang_tags)


def parse_opbd(font: Font, record: TableRecord) -> opbd: ...  # TODO: opbd


def parse_OS2(font: Font, record: TableRecord) -> OS2:
    font.seek(record.offset)
    version = font.get_uint16()
    xAvgCharWidth = font.get_FWORD()
    usWeightClass = font.get_uint16()
    usWidthClass = font.get_uint16()
    fsType = font.get_uint16()
    ySubscriptXSize = font.get_FWORD()
    ysubscriptYSize = font.get_FWORD()
    ySubscriptXOffset = font.get_FWORD()
    ySubscriptYOffset = font.get_FWORD()
    ySuperscriptXSize = font.get_FWORD()
    ySuperscriptYSize = font.get_FWORD()
    ySuperscriptXOffset = font.get_FWORD()
    ySuperscriptYOffset = font.get_FWORD()
    yStrikeoutSize = font.get_FWORD()
    yStrickoutPosition = font.get_FWORD()
    sFamilyClass = font.get_int16()
    panose = font.get_int8_array(10)
    ulUnicodeRange1 = font.get_uint32()
    ulUnicodeRange2 = font.get_uint32()
    ulUnicodeRange3 = font.get_uint32()
    ulUnicodeRange4 = font.get_uint32()
    achVendID = font.get_tag()
    fsSelection = font.get_uint16()
    usFirstCharIndex = font.get_uint16()
    usLastCharIndex = font.get_uint16()
    sTypoAscender = font.get_FWORD()
    sTypoDescender = font.get_FWORD()
    sTypeLineGap = font.get_FWORD()
    usWinAscent = font.get_UFWORD()
    usWinDescent = font.get_UFWORD()

    if version == 1:
        return OS2_v1(
            version,
            xAvgCharWidth,
            usWeightClass,
            usWidthClass,
            fsType,
            ySubscriptXSize,
            ysubscriptYSize,
            ySubscriptXOffset,
            ySubscriptYOffset,
            ySuperscriptXSize,
            ySuperscriptYSize,
            ySuperscriptXOffset,
            ySuperscriptYOffset,
            yStrikeoutSize,
            yStrickoutPosition,
            sFamilyClass,
            panose,
            ulUnicodeRange1,
            ulUnicodeRange2,
            ulUnicodeRange3,
            ulUnicodeRange4,
            achVendID,
            fsSelection,
            usFirstCharIndex,
            usLastCharIndex,
            sTypoAscender,
            sTypoDescender,
            sTypeLineGap,
            usWinAscent,
            usWinDescent,
            font.get_uint32(),
            font.get_uint32(),
        )
    elif version in {2, 3, 4}:
        return OS2_v4(
            version,
            xAvgCharWidth,
            usWeightClass,
            usWidthClass,
            fsType,
            ySubscriptXSize,
            ysubscriptYSize,
            ySubscriptXOffset,
            ySubscriptYOffset,
            ySuperscriptXSize,
            ySuperscriptYSize,
            ySuperscriptXOffset,
            ySuperscriptYOffset,
            yStrikeoutSize,
            yStrickoutPosition,
            sFamilyClass,
            panose,
            ulUnicodeRange1,
            ulUnicodeRange2,
            ulUnicodeRange3,
            ulUnicodeRange4,
            achVendID,
            fsSelection,
            usFirstCharIndex,
            usLastCharIndex,
            sTypoAscender,
            sTypoDescender,
            sTypeLineGap,
            usWinAscent,
            usWinDescent,
            font.get_uint32(),
            font.get_uint32(),
            font.get_FWORD(),
            font.get_FWORD(),
            font.get_uint16(),
            font.get_uint16(),
            font.get_uint16(),
        )
    elif version == 5:
        return OS2_v5(
            version,
            xAvgCharWidth,
            usWeightClass,
            usWidthClass,
            fsType,
            ySubscriptXSize,
            ysubscriptYSize,
            ySubscriptXOffset,
            ySubscriptYOffset,
            ySuperscriptXSize,
            ySuperscriptYSize,
            ySuperscriptXOffset,
            ySuperscriptYOffset,
            yStrikeoutSize,
            yStrickoutPosition,
            sFamilyClass,
            panose,
            ulUnicodeRange1,
            ulUnicodeRange2,
            ulUnicodeRange3,
            ulUnicodeRange4,
            achVendID,
            fsSelection,
            usFirstCharIndex,
            usLastCharIndex,
            sTypoAscender,
            sTypoDescender,
            sTypeLineGap,
            usWinAscent,
            usWinDescent,
            font.get_uint32(),
            font.get_uint32(),
            font.get_FWORD(),
            font.get_FWORD(),
            font.get_uint16(),
            font.get_uint16(),
            font.get_uint16(),
            font.get_uint16(),
            font.get_uint16(),
        )
    return OS2_v0(
        version,
        xAvgCharWidth,
        usWeightClass,
        usWidthClass,
        fsType,
        ySubscriptXSize,
        ysubscriptYSize,
        ySubscriptXOffset,
        ySubscriptYOffset,
        ySuperscriptXSize,
        ySuperscriptYSize,
        ySuperscriptXOffset,
        ySuperscriptYOffset,
        yStrikeoutSize,
        yStrickoutPosition,
        sFamilyClass,
        panose,
        ulUnicodeRange1,
        ulUnicodeRange2,
        ulUnicodeRange3,
        ulUnicodeRange4,
        achVendID,
        fsSelection,
        usFirstCharIndex,
        usLastCharIndex,
        sTypoAscender,
        sTypoDescender,
        sTypeLineGap,
        usWinAscent,
        usWinDescent,
    )


def parse_PCLT(font: Font, record: TableRecord) -> PCLT:
    font.seek(record.offset)
    return PCLT(
        font.get_uint16(),
        font.get_uint16(),
        font.get_uint32(),
        font.get_uint16(),
        font.get_uint16(),
        font.get_uint16(),
        font.get_uint16(),
        font.get_uint16(),
        font.get_uint16(),
        font.get_int8_array(16),
        font.get_int8_array(8),
        font.get_int8_array(6),
        font.get_int8(),
        font.get_int8(),
        font.get_uint8(),
        font.get_uint8(),
    )


def parse_post(font: Font, record: TableRecord) -> post:
    font.seek(record.offset)
    version = font.get_version_legacy()
    angle = font.get_fixed()
    underline_pos = font.get_FWORD()
    underline_thickness = font.get_FWORD()
    is_fixed_pitch = font.get_uint32()
    min_mem_type42 = font.get_uint32()
    max_mem_type42 = font.get_uint32()
    min_mem_type1 = font.get_uint32()
    max_mem_type1 = font.get_uint32()

    if version == (2, 0):
        count = font.get_uint16()
        glyph_name_index = font.get_uint16_array(count)
        return post_v2(
            version,
            angle,
            underline_pos,
            underline_thickness,
            is_fixed_pitch,
            min_mem_type42,
            max_mem_type42,
            min_mem_type1,
            max_mem_type1,
            count,
            glyph_name_index,
            tuple(
                font.read(font.get_uint8()).decode("utf-8")
                for i in glyph_name_index
                if i - 258 >= 0
            ),
        )
    elif version == (2, 5):
        count = font.get_uint16()
        offset = font.get_int8_array(count)
        return post_v25(
            version,
            angle,
            underline_pos,
            underline_thickness,
            is_fixed_pitch,
            min_mem_type42,
            max_mem_type42,
            min_mem_type1,
            max_mem_type1,
            count,
            offset,
        )
    return post_v1(
        version,
        angle,
        underline_pos,
        underline_thickness,
        is_fixed_pitch,
        min_mem_type42,
        max_mem_type42,
        min_mem_type1,
        max_mem_type1,
    )


def parse_prep(font: Font, record: TableRecord) -> prep: ...  # TODO: prep
def parse_prop(font: Font, record: TableRecord) -> prop: ...  # TODO: prop
def parse_sbix(font: Font, record: TableRecord) -> sbix: ...  # TODO: sbix
def parse_STAT(font: Font, record: TableRecord) -> STAT: ...  # TODO: STAT
def parse_SVG(font: Font, record: TableRecord) -> SVG: ...  # TODO: SVG
def parse_trak(font: Font, record: TableRecord) -> trak: ...  # TODO: trak
def parse_VDMX(font: Font, record: TableRecord) -> VDMX: ...  # TODO: VDMX
def parse_vhea(font: Font, record: TableRecord) -> vhea: ...  # TODO: vhea
def parse_vmtx(font: Font, record: TableRecord) -> vmtx: ...  # TODO: vmtx
def parse_VORG(font: Font, record: TableRecord) -> VORG: ...  # TODO: VORG
def parse_VVAR(font: Font, record: TableRecord) -> VVAR: ...  # TODO: VVAR
def parse_xref(font: Font, record: TableRecord) -> xref: ...  # TODO: xref
def parse_Zapf(font: Font, record: TableRecord) -> Zapf: ...  # TODO: Zapf


parsers: dict[str, ParseMethod] = {
    "acnt": parse_acnt,
    "ankr": parse_ankr,
    "avar": parse_avar,
    "BASE": parse_BASE,
    "bdat": parse_bdat,
    "bhed": parse_bhed,
    "bloc": parse_bloc,
    "bsln": parse_bsln,
    "CBDT": parse_CBDT,
    "CBLC": parse_CBLC,
    "CFF": parse_CFF,
    "CFF2": parse_CFF2,
    "cmap": parse_cmap,
    "COLR": parse_COLR,
    "CPAL": parse_CPAL,
    "cvar": parse_cvar,
    "cvt ": parse_cvt,
    "DSIG": parse_DSIG,
    "EBDT": parse_EBDT,
    "EBLC": parse_EBLC,
    "EBSC": parse_EBSC,
    "fdsc": parse_fdsc,
    "feat": parse_feat,
    "fmtx": parse_fmtx,
    "fond": parse_fond,
    "fpgm": parse_fpgm,
    "fvar": parse_fvar,
    "gasp": parse_gasp,
    "GDEF": parse_GDEF,
    "glyf": parse_glyf,
    "GPOS": parse_GPOS,
    "GSUB": parse_GSUB,
    "gvar": parse_gvar,
    "hdmx": parse_hdmx,
    "head": parse_head,
    "hhea": parse_hhea,
    "hmtx": parse_hmtx,
    "HVAR": parse_HVAR,
    "JSTF": parse_JSTF,
    "just": parse_just,
    "kern": parse_kern,
    "kerx": parse_kerx,
    "lcar": parse_lcar,
    "loca": parse_loca,
    "ltag": parse_ltag,
    "LTSH": parse_LTSH,
    "MATH": parse_MATH,
    "maxp": parse_maxp,
    "MERG": parse_MERG,
    "meta": parse_meta,
    "mort": parse_mort,
    "morx": parse_morx,
    "MVAR": parse_MVAR,
    "name": parse_name,
    "opbd": parse_opbd,
    "OS2": parse_OS2,
    "PCLT": parse_PCLT,
    "post": parse_post,
    "prep": parse_prep,
    "prop": parse_prop,
    "sbix": parse_sbix,
    "STAT": parse_STAT,
    "SVG": parse_SVG,
    "trak": parse_trak,
    "VDMX": parse_VDMX,
    "vhea": parse_vhea,
    "vmtx": parse_vmtx,
    "VORG": parse_VORG,
    "VVAR": parse_VVAR,
    "xref": parse_xref,
    "Zapf": parse_Zapf,
}

__all__ = ("ParseMethod", "parse_table_directory", "parsers")
