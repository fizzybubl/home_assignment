class ImmutableClass(type):

    def __setattr__(self, key, value):
        raise AttributeError("Can't modify values for an immutable class")


class StaticClass:

    def __new__(cls, *args, **kwargs):
        raise TypeError("Can't instantiate a static class")


class StaticImmutableClass(StaticClass, metaclass=ImmutableClass):
    ...
