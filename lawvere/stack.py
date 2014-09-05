# -*- coding: utf-8 -*-

def pipe(self, other):
    return self.__stacktype__.from_items(self, other)

def circle(self, other):
    return pipe(other, self)

def compose_with(stack_cls):
    def composable(cls):
        if not callable(cls): raise TypeError("Composables must be callable")
        if type(cls) != type:
            return stack_cls.from_vartype(cls)

        if is_composable(cls):
            return type(cls.__name__, (cls, ), {'__stacktype__': stack_cls})

        attributes = {
            '__stacktype__': stack_cls,
            'circle': circle,
            '__lshift__': circle,
            'pipe': pipe,
            '__rshift__': pipe
        }
        return type(cls.__name__, (cls, ), attributes)

    return composable


def compose_with_self(cls):
    return compose_with(property(lambda self: type(self)))(cls)

is_composable = lambda func: hasattr(func, '__stacktype__')

@compose_with_self
class Stack(tuple):
    @classmethod
    def from_vartype(cls, item):
        return cls(item if isinstance(item, tuple) else (item, ))

    @classmethod
    def from_items(cls, item1, item2):
        return cls.from_vartype(item1) + cls.from_vartype(item2)

    def __call__(self, *args, **kwargs):
        index = 0
        result = None
        for func in self:
            index += 1
            result = func(*args, **kwargs)
            if is_composable(result):
                return self.__stacktype__(self.from_vartype(result) + self[index:])
            args, kwargs = (result, ), {}
        return result

    def replace_at(self, key, item):
        return self[:key] + self.from_vartype(item) + self[key+1:]

    def replace(self, old, items):
        items = self.from_vartype(items)
        old = self.from_vartype(old)
        old_len = len(old)
        stack = self.__stacktype__()
        start_index = 0
        for found_index in self.iter_find(old):
            stack += self[start_index:found_index] + items
            start_index = found_index + old_len

        return stack + self[found_index + old_len:]

    def iter_find(self, items):
        items_len = len(items)
        i = 0
        while i <= len(self) - items_len:
            if self[i:i+items_len] == items:
                yield i
                i += items_len
            else:
                i += 1


    def without(self, items):
        return self.replace(items, tuple())

    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]

        return getattr(self[0], name)

    def __add__(self, other):
        return self.__addstacks__(self, other)

    def __radd__(self, other):
        return self.__addstacks__(other, self)

    def __addstacks__(self, stack1, stack2):
        return self.__stacktype__(tuple.__add__(stack1, stack2))

    def __getitem__(self, index):
        result = tuple.__getitem__(self, index)
        if isinstance(index, slice):
            result = self.__stacktype__(result)
        return result

    def __getslice__(self, i, j):
        return self.__getitem__(slice(i, j))


composable = compose_with(Stack)
