import operator
from pathlib import Path
import subprocess

from textual.events import Click, Event
import unicodedataplus as unicodedata

import rich.text
from fnt import FileFont
from fnt.exceptions import ParseError

from textual import work
from textual.app import App, ComposeResult
from textual.message import Message
from textual.screen import Screen, ModalScreen
from textual.containers import Horizontal, CenterMiddle, VerticalScroll, Vertical, Grid
from textual.widgets import DataTable, Header, Footer, ProgressBar, Label, Digits, Static, Rule, Button

from fnt.tables.cmap import cmapSubtable_v4

TABLES = (
    "acnt",
    "ankr",
    "avar",
    "BASE",
    "bdat",
    "bhed",
    "bloc",
    "bsln",
    "CBDT",
    "CBLC",
    "CFF",
    "CFF2",
    "cmap",
    "COLR",
    "CPAL",
    "cvar",
    "cvt",
    "DSIG",
    "EBDT",
    "EBLC",
    "EBSC",
    "fdsc",
    "feat",
    "fmtx",
    "fond",
    "fpgm",
    "fvar",
    "gasp",
    "GDEF",
    "glyf",
    "GPOS",
    "GSUB",
    "gvar",
    "hdmx",
    "head",
    "hhea",
    "hmtx",
    "HVAR",
    "JSTF",
    "just",
    "kern",
    "kerx",
    "lcar",
    "loca",
    "ltag",
    "LTSH",
    "MATH",
    "maxp",
    "MERG",
    "meta",
    "mort",
    "morx",
    "MVAR",
    "name",
    "opbd",
    "OS/2",
    "PCLT",
    "post",
    "prep",
    "prop",
    "sbix",
    "STAT",
    "SVG",
    "trak",
    "VDMX",
    "vhea",
    "vmtx",
    "VORG",
    "VVAR",
    "xref",
    "Zapf"
)

APPLE_ICON = "🍎"
WINDOWS_ICON = "🪟"

TABLE_DECS = {
    "acnt": f"Accent Attachment Table {APPLE_ICON}",
    "ankr": f"Anchor Point Table {APPLE_ICON}\nFor use with the [u]kerx[/u] table.",
    "avar": "Axis Variations\nUsed in variable fonts.",
    "BASE": f"Baseline Table {WINDOWS_ICON}\nUsed to align glyphs of different scripts and sizes in a line of text.",
    "bdat": f"Bitmap Data {APPLE_ICON}\nUsed in bitmap fonts.",
    "bhed": f"Bitmap Header {APPLE_ICON}\nUsed in bitmap fonts.",
    "bloc": f"Bitmap Location {APPLE_ICON}\nUsed in bitmap fonts.",
    "bsln": f"Baseline Table {APPLE_ICON}\nUsed to align glyphs of different scripts and sizes in a line of text.",
    "CBDT": f"Color Bitmap Data {WINDOWS_ICON}\nUsed in bitmap fonts.",
    "CBLC": f"Color Bitmap Header {WINDOWS_ICON}\nUsed in bitmap fonts.",
    "CFF":  f"Compact Font Format Representation (Version 1) {WINDOWS_ICON}\nIn accordance with Adobe Technical Notes #5176 and #5177.",
    "CFF2": f"Compact Font Format Representation (Version 2) {WINDOWS_ICON}\nAn alternative to the [u]glyf[/u] table.",
    "cmap": "Character Map\nDefines the mapping of character codes to a default glyph index.",
    "COLR": f"Color Table {WINDOWS_ICON}\nColor presentations for glyphs.",
    "CPAL": f"Color Palette Table {WINDOWS_ICON}\nOnly exists if [u]COLR[/u] is present.",
    "cvar": "CVT Variations\nVariations for the values in the [u]cvt [/u] table.",
    "cvt": "Control Value Table\nContains a list of variables used by instructions.",
    "DSIG": f"Digital Signatures {WINDOWS_ICON}",
    "EBDT": "Embdedded Bitmap Data Table",
    "EBLC": "Embedded Bitmap Location Table",
    "EBSC": "Embedded Bitmap Scaling Table",
    "fdsc": "Font Descriptors",
    "feat": f"Feature Name Table {APPLE_ICON}",
    "fmtx": "Font Metrics Table",
    "fond": "'Provides the ability to have true data-fork fonts to behave as if they were in a font suitcase with associated FOND data.'",
    "fpgm": "Font Program",
    "fvar": "Font Variations Table",
    "gasp": "Grid-fitting and Scan-conversion Procedure Table",
    "GDEF": "Glyph Definition Table",
    "glyf": "Glyph Data",
    "GPOS": "Glyph Positioning Table",
    "GSUB": "Glyph Substitution Table",
    "gvar": "Glyph Variations Table",
    "hdmx": "Horizontal Device Metrics",
    "head": "Font Header Table",
    "hhea": "Horizontal Header Table",
    "hmtx": "Horizontal Metrics Table",
    "HVAR": "Horizontal Metrics Variations Table",
    "JSTF": f"Justification Table {WINDOWS_ICON}",
    "just": f"Justification Table {APPLE_ICON}",
    "kern": "Kerning Table",
    "kerx": f"Kerning Table {APPLE_ICON}",
    "lcar": f"Ligature Caret Table {APPLE_ICON}",
    "loca": "Glyph Locations Table",
    "ltag": f"IETF Language Tags {APPLE_ICON}",
    "LTSH": "Linear Threshold Table",
    "MATH": "Mathematical Typesetting Table",
    "maxp": "Maximum Profile\nMaximum memory requirements for this font.",
    "MERG": "Merge Table\nDefines the order of compositing in respect to anti-aliasing.",
    "meta": "Metadata Table",
    "mort": f"Glyph Metamorphosis Table {APPLE_ICON}\n[bold red]DEPRECATED[/bold red]",
    "morx": f"Glyph Metamorphosis Table {APPLE_ICON}",
    "MVAR": "Metrics Variations Table",
    "name": "Naming Table\nMultilingual strings relating to this font.",
    "opbd": f"Optical Bounds Table {APPLE_ICON}",
    "OS/2": f"Metrics and Data Table {WINDOWS_ICON}\nRequired by Windows.",
    "PCLT": "PCL5 Language Table\nProvides compatibility with the Hewlett-Packard PCL 5 printer language",
    "post": "PostScript Table",
    "prep": "Control Value Program\nPreviously the 'pre-program' table.",
    "prop": f"Glyph Properties Table {APPLE_ICON}",
    "sbix": "Standard Bitmap Graphics Table\nAllows bitmap data in standard formats like PNG, TIFF, or JPEG.",
    "STAT": "Style Attributes Table",
    "SVG": "Scalable Vector Graphics Table",
    "trak": f"Tracking Table {APPLE_ICON}",
    "VDMX": "Vertical Device Metrics Table",
    "vhea": "Vertical Header Table",
    "vmtx": "Vertical Metrics Table",
    "VORG": "Vertical Origin Table",
    "VVAR": "Vertical Metrics Variations Table",
    "xref": f"Cross-Reference Table {APPLE_ICON}\nUsed by Apple font tools ftxdumperfuser and ftxenhancer, allowing the generation of other tables using symbolic names.",
    "Zapf": f"Individual Glyph Information {APPLE_ICON}\nNamed after legendary type designer Hermann Zapf."
}

FONT_PATH = "F:/!SORTED/Fonts"
FONT_EXTENSIONS = ("ttf", "otf", "fnt")

FONT_PATHS: list[Path] = []
for e in FONT_EXTENSIONS:
    FONT_PATHS.extend(Path(FONT_PATH).glob(f"*.{e}"))

LIMIT = min(10000, len(FONT_PATHS))

FONTS: list["Font"] = []

canon_tables = TABLES
fanon_tables = set()

def explore(path: Path):
    subprocess.run(['explorer', '/select,', path])

class Font:
    def __init__(self, file_font: FileFont, path: Path):
        self.file_font = file_font
        self.path = path

        self.table_records = {}
        for record in file_font.directory.tableRecords:
            if record.tableTag == "OS/2":
                self.table_records["OS/2"] = None  # TODO: This seems to be a bug in pyfont?
                continue
            try:
                self.table_records[record.tableTag] = getattr(file_font, record.tableTag)
            except (ParseError, AttributeError, UnicodeDecodeError):
                self.table_records[record.tableTag] = None

        self.char_ranges = []
        for subtable in file_font.cmap.subTables:
            if isinstance(subtable, cmapSubtable_v4):
                for s, e in zip(subtable.startCode, subtable.endCode, strict = True):
                    self.char_ranges.append((s, e))

        self.unicode_blocks = set()
        for s, e in self.char_ranges:
            for i in range(s, e + 1):
                self.unicode_blocks.add(unicodedata.block(chr(i)))

    @property
    def family(self) -> str:  # type: ignore -- typing is mad but I don't care
        try:
            record = None
            for record in self.file_font.name.nameRecords:
                if record.nameID == 1:
                    return record.string
            if record is None:
                return ERROR
        except Exception:
            return ERROR
        
    @property
    def weight(self) -> str | None:
        try:
            record = None
            for record in self.file_font.name.nameRecords:
                if record.nameID == 2:
                    return record.string
            if record is None:
                return ERROR
        except Exception:
            return ERROR
        
    @property
    def display_name(self) -> str:
        if self.weight and self.weight != ERROR:
            return f"{self.family} {self.weight}"
        elif self.family != ERROR:
            return self.family
        else:
            return ERROR
        
    @property
    def tables(self) -> list[str]:
        tables = []
        for record in self.file_font.directory.tableRecords:
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
    
# --- BEGIN TEXTUAL APP ---

ERROR = rich.text.Text("ERROR", style = "dim italic")
NO_BLOCK = "[dim][italic]No Block[/italic][/dim]"
YES = "✅"
NO = "❌"

class Loaded(Message):
    ...

class LoadingScreen(Screen):
    def __init__(self, *, name = None, id = None, classes = None):
        super().__init__(name, id, classes)
        self.font_total = 0

        self.classes = "centered_screen"

    def compose(self) -> ComposeResult:
        yield Header()
        with CenterMiddle(classes = "hello"):
            yield Digits("0", classes = "hello_element")
            yield ProgressBar(total = LIMIT, show_eta = False, classes = "hello_element")
        yield Label("...", classes = "hello_text")
        yield Footer()

    def on_mount(self) -> None:
        self.load_fonts()

    def on_loaded(self):
        self.app.push_screen(TableScreen())

    @work(thread = True)
    def load_fonts(self):
        for font_path in FONT_PATHS[:LIMIT]:
            label = self.query_one(Label)
            label.content = str(font_path)
            with font_path.open(mode = "rb") as f:
                font_bytes = f.read()
            file_font = FileFont(font_bytes, font_path)
            font = Font(file_font, font_path)
            self.app.fonts.append(font)
            for table in font.tables:
                if table not in canon_tables:
                    fanon_tables.add(table)
                if table not in self.app.tables:
                    self.app.tables[table] = 1
                else:
                    self.app.tables[table] += 1
            bar = self.query_one(ProgressBar)
            self.app.call_from_thread(bar.advance, 1)
            self.font_total += 1
            digits = self.query_one(Digits)
            self.app.call_from_thread(digits.update, str(self.font_total))
        self.post_message(Loaded())

class SummaryScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Back")]

    def __init__(self, *, name = None, id = None, classes = None):
        super().__init__(name, id, classes)
        
        self.sorted_tables = sorted(self.app.tables.items(), key=operator.itemgetter(1), reverse = True)
        self.unused_tables = [table for table in canon_tables if table not in self.app.tables.keys()]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Fonts loaded:")
        yield Digits(str(len(self.app.fonts)))
        yield Rule()
        with VerticalScroll():
            for table, value in self.sorted_tables:
                with Horizontal():
                    yield Label(table)
                    yield ProgressBar(LIMIT, id = (f"bar_{table}".strip() if table != "OS/2" else "bar_os2"), show_eta = False)
                    yield Label(f" | {value}")
            yield Static(f"Unused Tables: {', '.join(self.unused_tables)}")
        yield Footer()

    def on_mount(self) -> None:
        for table, value in self.sorted_tables:
            bar = self.get_widget_by_id(f"bar_{table}".strip() if table != "OS/2" else "bar_os2")
            bar.advance(value)


class TableInfoScreen(ModalScreen):
    def __init__(self, table_name: str, name: str | None = None, id: str | None = None, classes: str | None = None):
        super().__init__(name, id, classes)
        self.table_name = table_name

    def compose(self) -> ComposeResult:
        yield Vertical(
            Label(TABLE_DECS[self.table_name] if self.table_name in TABLE_DECS else f"Unknown Table: {self.table_name}", id="question"),
            Button("Close", id="quit"),
            id="dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "quit":
            self.app.pop_screen()

class TableNameStatic(Static):
    def __init__(self, content = "", *, expand: bool = False, shrink: bool = False, markup: bool = True, name: str | None = None, id: str | None = None, classes: str | None = None, disabled: bool = False) -> None:
        super().__init__(content, expand=expand, shrink=shrink, markup=markup, name=name, id=id, classes=classes, disabled=disabled)

    def on_event(self, event: Event):
        if isinstance(event, Click):
            self.app.push_screen(TableInfoScreen(str(self.content)))
        return super().on_event(event)


class FontScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Back")]

    def __init__(self, font: Font, *, name = None, id = None, classes = None):
        super().__init__(name, id, classes)
        self.font = font

    def compose(self) -> ComposeResult:
        sidebar_text = f"[italic]File Name[/italic]\n{self.font.path.name}\n\n[italic]Glyph Count[/italic]\n{self.font.char_count}\n\n[italic]Tables[/italic]\n"

        blocks = ""
        for block in self.font.unicode_blocks:
            blocks += (block + "\n" if block != "No_Block" else NO_BLOCK + "\n")

        yield Header()
        with Vertical():
            with Horizontal():
                with Vertical(id = "sidebar"):
                    yield Static(sidebar_text)
                    for table in self.font.tables:
                        yield TableNameStatic(table)
                with Vertical():
                    yield Static(f"{self.font.display_name}", classes = "body")
                    yield Static("[italic]Supported Blocks[/italic]", classes = "body")
                    with VerticalScroll(classes = "body_text"):
                        yield Static(blocks)
        yield Footer()

    def on_mount(self) -> None:
        ...

class TableScreen(Screen):
    BINDINGS = [("s", "summary_screen", "Summary")]

    def __init__(self, *, name = None, id = None, classes = None):
        super().__init__(name, id, classes)
        self.last_clicked_header = "font_name"
        self.reverse = False

        self.classes = "centered_screen"

    def compose(self) -> ComposeResult:
        yield Header()
        yield DataTable(id = "table", fixed_columns = 1, zebra_stripes = True)
        yield Footer()

    def on_show(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(("Name", "font_name"), ("T#", "table_count"))
        for t in canon_tables:
            table.add_column(t, key = t)
        for t in fanon_tables:
            table.add_column(t, key = t)
        table.add_column("Path", key = "file_name")

        table.loading = True
        self.add_fonts(table)

    @work(thread = True)
    def add_fonts(self, table: DataTable) -> None:
        for font in self.app.fonts:
            tables = []
            for t in canon_tables:
                tables.append(YES if t in font.tables else NO)
            for t in fanon_tables:
                tables.append(YES if t in font.tables else NO)
            self.app.call_from_thread(table.add_row, font.display_name, font.table_count, *tables, font.path.name)

        table.sort("font_name", key = lambda x: str(x).casefold())
        table.loading = False

    def on_data_table_cell_selected(self, event: DataTable.CellSelected) -> None:
        self.log(event.cell_key.row_key.value, event.cell_key.column_key.value, event.value)
        if event.cell_key.column_key.value == "file_name":
            explore(Path(FONT_PATH) / str(event.value))
        if event.cell_key.column_key.value == "font_name":
            font_path = event.data_table.get_row_at(event.coordinate.row)[-1]
            font = [font for font in self.app.fonts if font.path.name == font_path][0]
            self.app.push_screen(FontScreen(font))

    def on_data_table_header_selected(self, event: DataTable.HeaderSelected) -> None:
        if self.last_clicked_header == event.column_key:
            self.reverse = not self.reverse
        else:
            self.reverse = False
        self.last_clicked_header = event.column_key

        event.data_table.sort(event.column_key, key = lambda x: str(x).casefold(), reverse = self.reverse)

    def action_summary_screen(self):
        self.app.push_screen(SummaryScreen())
    
class FontApp(App):
    CSS_PATH = "./run.tcss"

    def __init__(self):
        super().__init__()
        self.fonts: list[Font] = []
        self.tables: dict[str, int] = {}
        self.fonts_loaded = False

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()

    async def on_mount(self) -> None:
        self.title = "PyFont"
        self.theme = "nord"

        self.push_screen(LoadingScreen())

app: App = FontApp()

def run():
    app.run()
