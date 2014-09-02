# -*- coding: utf-8 -*-
from .arrow import Arrow


class Dispatcher(list):
    wrap = Arrow
    def __init__(self, items=list(), args=tuple(), kwargs=dict(), name='Dispatcher'):
        list.__init__(self, items)
        self.args = args
        self.kwargs = kwargs
        self.__name__ = name

    def __call__(self, *args, **kwargs):
        args = self.args + args
        kwargs.update(self.kwargs)
        items = tuple(filter(lambda item: item.accept(args, kwargs), self))
        items_len = len(items)
        if  items_len == 1:
            return items[0](*args, **kwargs)
        if items_len > 1:
            return type(self)(items, args, kwargs, self.__name__)

        raise TypeError('"%s" signature don\'t allow (%s) as parameters' % (self.__name__, self.parameters_str(args, kwargs)))

    def parameters_str(self, args, kwargs):
        parameters = list()
        if len(args) == 1:
            parameters = [str(args)[1:-2], ]
        else:
            parameters = str(args)[1:-1].split(', ')
        if len(kwargs) > 0:
            kwargs = zip(kwargs.keys(), str(kwargs.values())[1:-1].split(', '))
            parameters.extend(('%s=%s' %(name, value) for name, value in kwargs))
        return ', '.join(parameters)

    def append(self, item):
        list.append(self, item)
        return item

    def register(self, *args, **kwargs):
        result = self.wrap(*args, **kwargs)
        if isinstance(result, type(self.wrap)):
            return result.append(self.append)
        return self.append(result)

    @classmethod
    def build(cls, *args, **kwargs):
        result = cls.wrap(*args, **kwargs)
        if isinstance(result, type(cls.wrap)):
            return result.append(cls.dispatch)

        return cls.dispatch(result)

    @classmethod
    def dispatch(cls, func):
        return cls([func, ], name=getattr(func, '__name__', cls.__name__))

def dispatcher(wrapper):
    return type('Dispatcher', (Dispatcher, ), {'wrap': Arrow.wrap(wrapper)}).build

