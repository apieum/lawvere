# -*- coding: utf-8 -*-

class Arrow(object):
    __functype__ = lambda self, func: func
    def __init__(self, domain, codomain):
        self.domain = domain
        self.codomain = codomain

    def __call__(self, func):
        domain = isinstance(self.domain, tuple) and self.domain or (self.domain, )
        setattr(func, 'domain', domain)
        setattr(func, 'codomain', self.codomain)
        return self.__functype__(func)


def ArrowType(cls):
    return type('Arrow', (Arrow, ), {'__functype__': cls})
