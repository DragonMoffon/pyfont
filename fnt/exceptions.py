class MissingTableError(KeyError):
    def __init__(self, table_name: str, *args):
        super().__init__(f"font does not contain the {table_name} table.", *args)

class ParseError(ValueError):
    def __init__(self, table_name: str, *args):
        super().__init__(f"failed to parse the {table_name} table", *args)
