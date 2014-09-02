# -*- coding: utf-8 -*-
from .curry import Curry
Default = type('Default', (tuple, ), {})()

class MultipleWrap(object):
    def __init__(self, factory, wrappers=tuple()):
        self.factory = factory
        self.wrappers = wrappers

    def __call__(self, *args, **kwargs):
        try:
            return self.wrap(self.factory(*args, **kwargs))
        except ValueError:
            return self.apply(*args, **kwargs)

    def wrap(self, wrapper):
        return type(self)(self.factory, (wrapper, ) + self.wrappers)

    def apply(self, *args, **kwargs):
        for wrapper in self.wrappers:
            args, kwargs = (wrapper(*args, **kwargs), ), {}
        return args[0]


def factory(domain=Default, codomain=Default):
    if type(domain) == type:
        domain = (domain, )

    if callable(domain):
        raise ValueError("Domain callable")

    return typedef(domain, codomain)


def annotate(func, domain, codomain=Default):
    varnames = getattr(func.__code__, 'co_varnames', tuple())
    annotations = getattr(func, '__annotations__', {})
    annotations.update(zip(varnames, domain))
    if codomain is not Default:
        annotations['return'] = codomain
    setattr(func, '__annotations__', annotations)
    return func

def typedef(domain, codomain=Default):
    return lambda func: annotate(func, domain, codomain)

Arrow = MultipleWrap(factory)
