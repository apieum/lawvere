# -*- coding: utf-8 -*-

def tupleize(item, tuple_type=tuple):
    return tuple_type(item if isinstance(item, tuple) else (item, ))

def compose_with(stack_cls):
    def composable(cls):
        if not callable(cls): raise TypeError("Composables must be callable")
        if type(cls) != type:
            return stack_cls((cls, ))

        if is_composable(cls):
            return type(cls.__name__, (cls, ), {'__composable__': stack_cls})

        def pipe(self, other):
            return self.__composable__(tupleize(self, self.__composable__) + tupleize(other, self.__composable__))

        def circle(self, other):
            return pipe(other, self)

        attributes = {
            '__composable__': stack_cls,
            'circle': circle,
            '__lshift__': circle,
            'pipe': pipe,
            '__rshift__': pipe
        }
        return type(cls.__name__, (cls, ), attributes)

    return composable


def compose_with_self(cls):
    cls = compose_with(cls)(cls)
    setattr(cls, '__composable__', cls)
    return cls

is_composable = lambda func: hasattr(func, '__composable__')

@compose_with_self
class Stack(tuple):
    def __call__(self, *args, **kwargs):
        index = 0
        result = None
        for func in self:
            index += 1
            result = func(*args, **kwargs)
            if is_composable(result):
                return self.__composable__(tupleize(result) + self[index:])
            args, kwargs = (result, ), {}
        return result

    def replace_at(self, key, item):
        result = list(self)
        result[key] = item
        return self.__composable__(result)

    def replace(self, old, items):
        items = tupleize(items)
        old = tupleize(old)
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

    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        if len(self) == 1:
            return getattr(self[0], name)

        raise AttributeError('%s not set' % name)


composable = compose_with(Stack)
