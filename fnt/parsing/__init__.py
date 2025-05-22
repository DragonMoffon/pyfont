from math import log2, floor

from fnt.font import Font, ParseMethod
from fnt.tables import (
    TableRecord,
    TableDirectory,
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
    head,
    hhea,
    LongHorMetric,
    hmtx,
    maxp,
    maxp_v05,
    maxp_v10,
    name,
    NameRecord,
    LangTagRecord,
    name_v0,
    name_v1,
    OS2,
    OS2_v0,
    OS2_v1,
    OS2_v5,
    OS2_v4,
    post,
    post_v1,
    post_v2,
    post_v25,
)
from fnt.flags import Platform, WindowsEncoding, MacintoshEncoding


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

            # TODO: get actual id array
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
                (),
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


parsers: dict[str, ParseMethod] = {
    "cmap": parse_cmap,
    "head": parse_head,
    "hhea": parse_hhea,
    "maxp": parse_maxp,
    "hmtx": parse_hmtx,
    "name": parse_name,
    "OS/2": parse_OS2,
    "post": parse_post,
}

__all__ = ("ParseMethod", "parse_table_directory", "parsers")
