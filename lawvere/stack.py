# -*- coding: utf-8 -*-

def compose_with(stack_cls):
    def composable(cls):
        if not callable(cls): raise TypeError("Composables must be callable")
        if type(cls) != type:
            return stack_cls.from_vartype(cls)

        if is_composable(cls):
            return type(cls.__name__, (cls, ), {'__stacktype__': stack_cls})

        def pipe(self, other):
            return self.__stacktype__.from_items(self, other)

        def circle(self, other):
            return pipe(other, self)

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
    cls = compose_with(cls)(cls)
    setattr(cls, '__stacktype__', cls)
    return cls

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
        result = list(self)
        result[key] = item
        return self.__stacktype__(result)

    def replace(self, old, items):
        items = self.from_vartype(items)
        old = self.from_vartype(old)
        old_len = len(old)
        stack = tuple()
        start_index = 0
        for found_index in self.iter_find(old):
            stack += self[start_index:found_index] + items
            start_index = found_index + old_len

        stack += self[found_index + old_len:]
        return self.__stacktype__(stack)

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
        if len(self) == 1:
            return getattr(self[0], name)

        raise AttributeError('%s not set' % name)

    def __add__(self, other):
        return self.__stacktype__(tuple.__add__(self, other))

    def __radd__(self, other):
        return self.__stacktype__(tuple.__add__(other, self))


composable = compose_with(Stack)
