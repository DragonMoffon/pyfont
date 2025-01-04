# Abstract
class Font:

    def __init__():
        pass

    def get_tables():
        pass

    def get_table(name: str):
        pass

    def has_table(name: str) -> bool:
        pass

    def is_table_parsed(name: str) -> bool:
        pass


# File Fonts hold and manage their own byte data. They can do what the like with it, and
# aren't beholdent to a collection.
class FileFont:
    pass


# Collection Fonts have less control over their own bytes, and need to ask the Collection
# for some data, this should have no impact on the end user
class CollectionFont:
    pass


class Collection:
    pass
