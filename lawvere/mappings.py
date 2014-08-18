# -*- coding: utf-8 -*-

class Arrow(object):
    __wrapper__ = lambda self, func: func
    def __init__(self, domain, codomain):
        self.domain = domain
        self.codomain = codomain

    def __call__(self, func):
        setattr(func, 'domain', self.domain)
        setattr(func, 'codomain', self.codomain)
        return self.__wrapper__(func)


def ArrowType(cls):
    return type('Arrow', (Arrow, ), {'__wrapper__': cls})
