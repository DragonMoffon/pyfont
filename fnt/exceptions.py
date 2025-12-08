class MissingFontError(KeyError):
    def __init__(self, idx: int, *args: object) -> None:
        super().__init__(f"Collection does not contain {idx + 1} fonts", *args)

class MissingTableError(KeyError):
    def __init__(self, table_name: str, *args):
        super().__init__(f"font does not contain the {table_name} table", *args)

class ParseError(ValueError):
    def __init__(self, table_name: str, *args):
        super().__init__(f"failed to parse the {table_name} table", *args)
