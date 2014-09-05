# -*- coding: utf-8 -*-
from .typify import typify, typed

def parameters_str(args, kwargs):
    parameters = list()
    if len(args) == 1:
        parameters = [str(args)[1:-2], ]
    else:
        parameters = str(args)[1:-1].split(', ')
    if len(kwargs) > 0:
        kwargs = zip(kwargs.keys(), str(kwargs.values())[1:-1].split(', '))
        parameters.extend(('%s=%s' %(name, value) for name, value in kwargs))
    return ', '.join(parameters)


class Dispatcher(object):
    wrap = typed
    def __init__(self, funcs, args=tuple(), kwargs=dict()):
        self.funcs = funcs
        self.args = args
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        args = self.args + args
        kwargs.update(self.kwargs)
        items = tuple(filter(lambda item: item.accept(args, kwargs), self.funcs))
        items_len = len(items)
        if  items_len == 1:
            return items[0](*args, **kwargs)
        if items_len > 1:
            return type(self)(items, args, kwargs)

        raise TypeError('"%s" signature doesn\'t allow (%s) as parameters' % (self.__name__, parameters_str(args, kwargs)))

    @property
    def __name__(self):
        return getattr(self.funcs[0], '__name__', type(self).__name__)

    def __iter__(self):
        return iter(self.funcs)

    def __getattr__(self, name):
        if name in ('register', '__call__'):
            return self.__dict__[name]
        return getattr(self.funcs[0],  name, self.__dict__.get(name))

    def __lshift__(self, other):
        return self.funcs[0].__lshift__(other)

    def __rshift__(self, other):
        return self.funcs[0].__rshift__(other)

    def register(self, *args, **kwargs):
        append = lambda item: self.funcs.append(item) or item
        result = self.wrap(*args, **kwargs)
        if isinstance(result, type(self.wrap)):
            return result.append(append)
        return append(result)

    @classmethod
    def dispatch(cls, *args, **kwargs):
        result = cls.wrap(*args, **kwargs)
        if isinstance(result, type(cls.wrap)):
            return result.append(cls.build)

        return cls.build(result)

    @classmethod
    def build(cls, func):
        return cls([func, ])

def dispatcher(wrapper):
    return type('Dispatcher', (Dispatcher, ), {'wrap': typify(wrapper)}).dispatch

dispatch = Dispatcher.dispatch
