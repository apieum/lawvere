# -*- coding: utf-8 -*-
from .morphism import Morphism

class Arrow(object):
    def __init__(self, domain, codomain):
        self.domain = domain
        self.codomain = codomain

    def __call__(self, func):
        setattr(func, 'domain', self.domain)
        setattr(func, 'codomain', self.codomain)
        return Morphism(func)
