class InvalidFieldTypeError(Exception):

    def __init__(self, entry: str):
        Exception.__init__(self, f"Table field type {entry} is not supported")


class MissingVersionFieldError(Exception):

    def __init__(self, cls: type):
        Exception.__init__(self, f"The versioned tabled {cls} must have version fields")


class IllformedTTFTypeError(Exception):

    def __init__(self, cls: type):
        Exception.__init__(self, f"{cls} is not a fully formed TTF type")


class TableRedefinitionError(Exception):
    def __init__(self, cls: type):
        Exception.__init__(
            self, f"{cls} has already been defined, use {cls}.version(<x>) instead."
        )
