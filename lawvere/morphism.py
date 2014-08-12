# -*- coding: utf-8 -*-
from .curry import Curry
from .signatures import use_signature, Signature

class MorphismSignature(Signature):
    pass

@use_signature(MorphismSignature)
class Morphism(Curry):
    pass

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
        self.codomain = None

    def __rshift__(self, mapping):
        mapping = getattr(mapping, 'codomain', mapping)
        return Arrow(self.domain, mapping)

class Codomain(Mapping):
    def __init__(self, codomain):
        self.domain = None
        self.codomain = codomain


