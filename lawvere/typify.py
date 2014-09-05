# -*- coding: utf-8 -*-
Default = type('Default', (tuple, ), {})()

class MultipleWrap(object):
    def __init__(self, factory, wrappers=tuple()):
        self.factory = factory
        self.wrappers = wrappers

    def __call__(self, *args, **kwargs):
        if self.factory.accept(*args, **kwargs):
            return self.wrap(self.factory(*args, **kwargs))
        else:
            return self.apply(*args, **kwargs)

    def wrap(self, wrapper):
        return type(self)(self.factory, (wrapper, ) + self.wrappers)

    def append(self, wrapper):
        return type(self)(self.factory, self.wrappers + (wrapper, ))

    def apply(self, *args, **kwargs):
        for wrapper in self.wrappers:
            args, kwargs = (wrapper(*args, **kwargs), ), {}
        return args[0]


class Factory(object):
    def __init__(self, domain=Default, codomain=Default):
        self.domain = domain
        self.codomain = codomain

    def __call__(self, func):
        return annotate(func, self.domain, self.codomain)

    @classmethod
    def accept(cls, domain=Default, codomain=Default):
        return type(domain) == type or not callable(domain)


def annotate(func, domain=Default, codomain=Default):
    if not isinstance(domain, tuple):
        domain = (domain, )
    varnames = getattr(func.__code__, 'co_varnames', tuple())
    annotations = getattr(func, '__annotations__', {})
    annotations.update(zip(varnames, domain))
    if codomain is not Default:
        annotations['return'] = codomain
    setattr(func, '__annotations__', annotations)
    return func

def typedef(domain=Default, codomain=Default):
    return lambda func: annotate(func, domain, codomain)

typed = MultipleWrap(Factory)
typify = typed.wrap
