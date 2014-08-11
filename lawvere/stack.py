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
        result = list(self)
        result[key] = item
        return self.__composable__(result)

    def replace(self, old, item):
        replace = lambda func: func == old and item or func
        return self.__composable__(map(replace, self))

    def without(self, items):
        return self.__composable__(tuple(self.iter_without(items)))

    def iter_without(self, items):
        items = self.tupleize(items)
        i = 0
        items_len = len(items)
        self_len = len(self)
        while i <= self_len - items_len:
            if self[i:i+items_len] != items:
                yield self[i]
                i+=1
            else:
                i += items_len
        for item in self[i:self_len]:
            yield item

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
