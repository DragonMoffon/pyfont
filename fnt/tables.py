from __future__ import annotations

from dataclasses import dataclass

from .types import Table, uint32_t, uint16_t, Tag_t, Offset32_t


# TableDirectory
@dataclass
class TableDirectory(Table):
    sfntVersion: uint32_t
    numTables: uint16_t
    searchRange: uint16_t
    entrySelector: uint16_t
    rangeShift: uint16_t


@dataclass
class TableRecord(Table):
    tableTag: Tag_t
    checksum: uint32_t
    offset: Offset32_t
    lenght: uint32_t
