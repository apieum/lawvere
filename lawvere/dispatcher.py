# -*- coding: utf-8 -*-
from .arrow import Arrow


class DispatchResolver(list):
    wrap = Arrow
    def __init__(self, items, args=tuple(), kwargs=dict(), name='Dispatcher'):
        list.__init__(self, items)
        self.args = args
        self.kwargs = kwargs
        self.name = name

    def __call__(self, *args, **kwargs):
        args = self.args + args
        kwargs.update(self.kwargs)
        items = tuple(filter(lambda item: item.accept(args, kwargs), self))
        items_len = len(items)
        if  items_len == 1:
            return items[0](*args, **kwargs)
        if items_len > 1:
            return DispatchResolver(items, args, kwargs, self.name)

        raise ValueError('Function "%s" not exists for parameters: (%s)' % (self.name, self.parameters_str(args, kwargs)))

    def parameters_str(self, args, kwargs):
        parameters = list()
        if len(args) == 1:
            parameters = [str(args)[1:-2], ]
        else:
            parameters = str(args)[1:-1].split(', ')
        parameters.extend(str(kwargs)[1:-1].split(', '))
        return ', '.join(parameters).replace(': ', '=')

    def append(self, item):
        list.append(self, item)
        return item

    def register(self, *args, **kwargs):
        result = self.wrap(*args, **kwargs)
        if isinstance(result, type(self.wrap)):
            return result.append(self.append)
        return self.append(result)

def dispatcher(wrapper):
    wrapper = Arrow.wrap(wrapper)
    resolver = type('Dispatcher', (DispatchResolver, ), {'wrap': wrapper})
    def dispatch(*args, **kwargs):
        dispatcher = resolver(list())
        result = dispatcher.register(*args, **kwargs)
        if isinstance(result, type(dispatcher.wrap)):
            return result.append(lambda *args: dispatcher)
        return dispatcher
    return dispatch

