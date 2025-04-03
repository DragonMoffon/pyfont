from .font import Font


# Collection Fonts have less control over their own bytes, and need to ask the Collection
# for some data, this should have no impact on the end user
class CollectionFont(Font):
    pass


class Collection:
    pass
