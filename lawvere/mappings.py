# -*- coding: utf-8 -*-
from .morphism import Morphism

class Mapping(object):
    def __call__(self, func):
        setattr(func, 'domain', self.domain)
        setattr(func, 'codomain', self.codomain)
        return Morphism(func)


class Arrow(Mapping):
    def __init__(self, domain, codomain):
        self.domain = domain
        self.codomain = codomain


class Domain(Mapping):
    def __init__(self, domain):
        self.domain = domain
        self.codomain = tuple()

    def __rshift__(self, mapping):
        codomain = getattr(mapping, 'codomain', mapping)
        return Arrow(self.domain, codomain)

class Codomain(Mapping):
    def __init__(self, codomain):
        self.domain = tuple()
        self.codomain = codomain


