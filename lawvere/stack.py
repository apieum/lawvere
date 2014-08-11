# -*- coding: utf-8 -*-

def compose_with(stack_cls):
    def composable(cls):
        if not callable(cls): raise TypeError("Composables must be callable")
        if type(cls) != type:
            return stack_cls((cls, ))

        if is_composable(cls):
            return cls

        def circle(self, other):
            if not isinstance(other, tuple):
                return self.__composable__((self, other))
            return self.__composable__((self, ) + other)

        def pipe(self, other):
            if not isinstance(other, tuple):
                return self.__composable__((other, self))
            return self.__composable__(other + (self, ))
        prop = {
            '__composable__': stack_cls,
            'circle': circle,
            '__mul__': circle,
            'pipe': pipe,
            '__rshift__': pipe
        }
        return type(cls.__name__, (cls, ), prop)

    return composable


def compose_with_self(cls):
    return compose_with(cls)(cls)

is_composable = lambda func: hasattr(func, '__composable__')

class Stack(tuple):
    def __call__(self, *args, **kwargs):
        index = 0
        result = None
        for func in self:
            result = func(*args, **kwargs)
            if is_composable(result):
                return self.__composable__(self.tupleize(result) + self[index+1:])
            args, kwargs = (result, ), {}
            index += 1
        return result

    def replace_at(self, key, item):
        result = tuple(self)
        result[key] = item
        return self.__composable__(result)

    def replace(self, old, items):
        items = self.tupleize(items)
        old = self.tupleize(old)
        old_len = len(old)
        stack = tuple()
        start_index = 0
        for found_index in self.iter_find(old):
            stack += self[start_index:found_index] + items
            start_index = found_index + old_len

        stack += self[found_index + old_len:]
        return self.__composable__(stack)

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

    def pipe(self, other):
        return self.__composable__(self + self.tupleize(other))

    def circle(self, other):
        return self.__composable__(self.tupleize(other) + self)

    def tupleize(self, item):
        return item if isinstance(item, tuple) else (item, )

    __rshift__ = pipe
    __mul__ = circle

setattr(Stack, '__composable__', Stack)
composable = compose_with(Stack)
