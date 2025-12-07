from pathlib import Path
import unicodedataplus as unicodedata

import rich.text
from fnt.exceptions import ParseError
from fnt.file_font import FileFont
from fnt.tables.cmap import cmapSubtable_v4

ERROR = rich.text.Text("ERROR", style = "dim italic")

class Font:
    def __init__(self, file_font: FileFont, path: Path):
        self.file_font = file_font
        self.path = path

        self.table_records = {}
        for table_name in file_font.get_table_names():
            try:
                self.table_records[table_name] = file_font.get_table(table_name)
            except (ParseError, KeyError, UnicodeDecodeError):
                self.table_records[table_name] = None

        self.char_ranges = []
        for subtable in file_font.cmap.subTables:  # type: ignore -- .cmap is basically guaranteed
            if isinstance(subtable, cmapSubtable_v4):
                for s, e in zip(subtable.startCode, subtable.endCode, strict = True):
                    self.char_ranges.append((s, e))

        self.unicode_blocks = set()
        for s, e in self.char_ranges:
            for i in range(s, e + 1):
                self.unicode_blocks.add(unicodedata.block(chr(i)))  # type: ignore -- unicodedataplus monkeypatches this

    @property
    def family(self) -> str | rich.text.Text:  # type: ignore -- will never be None
        try:
            record = None
            for record in self.file_font.name.nameRecords:  # type: ignore -- will never be None
                if record.nameID == 1:
                    return record.string
            if record is None:
                return ERROR
        except Exception:
            return ERROR
        
    @property
    def weight(self) -> str | rich.text.Text:  # type: ignore -- will never be None
        try:
            record = None
            for record in self.file_font.name.nameRecords:  # type: ignore -- will never be None
                if record.nameID == 2:
                    return record.string
            if record is None:
                return ERROR
        except Exception:
            return ERROR
        
    @property
    def display_name(self) -> str | rich.text.Text:
        if self.weight and self.weight != ERROR:
            return f"{self.family} {self.weight}"
        elif self.family != ERROR:
            return self.family
        else:
            return ERROR
        
    @property
    def tables(self) -> list[str]:
        tables = []
        for record in self.file_font.directory.tableRecords:  # type: ignore -- will never be None
            tables.append(record.tableTag)
        return tables
    
    @property
    def table_count(self) -> int:
        return len(self.tables)
    
    @property
    def char_count(self) -> int:
        count = 0
        for s, e in self.char_ranges:
            count += (e - s) + 1
        return count
