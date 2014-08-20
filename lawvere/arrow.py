# -*- coding: utf-8 -*-

class Arrow(object):
    __functype__ = lambda self, func: func
    def __init__(self, domain=tuple(), codomain=None):
        self.domain = domain
        self.codomain = codomain

    def __call__(self, func):
        domain = isinstance(self.domain, tuple) and self.domain or (self.domain, )
        varnames = getattr(func.__code__, 'co_varnames', tuple())
        annotations = dict(zip(varnames, domain))
        annotations['return'] = self.codomain
        annotations.update(getattr(func, '__annotations__', {}))
        setattr(func, '__annotations__', annotations)
        return self.__functype__(func)


def ArrowType(cls):
    return type('Arrow', (Arrow, ), {'__functype__': cls})
