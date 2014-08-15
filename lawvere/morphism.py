# -*- coding: utf-8 -*-
from .curry import Curry
from .signatures import use_signature, Signature

class MorphismSignature(Signature):
    def __init__(self, args, kwargs, domain=tuple(), codomain=tuple()):
        Signature.__init__(self, args, kwargs)
        self.domain = domain
        self.codomain = codomain

    @classmethod
    def from_func(cls, func):
        domain = getattr(func, 'domain', tuple())
        codomain = getattr(func, 'codomain', tuple())
        signature = cls(*cls.inspect_parameters(func), domain=domain, codomain=codomain)
        return signature

    @property
    def domain(self):
        return self.__dict__.get('domain')

    @domain.setter
    def domain(self, domain):
        if not isinstance(domain, tuple):
            domain = (domain, )
        self.__dict__['domain'] = domain


    def assert_domain_valid(self, args, domain):
        if len(args) != len(domain):
            raise TypeError("Domain not valid")
        index = 0
        for name, arg in args:
            if not isinstance(arg, domain[index]):
                raise TypeError("Argument %s not in domain" % name)
            index +=1

    def assert_codomain_valid(self, result, codomain):
        if not isinstance(result, codomain):
            raise TypeError("Result not in codomain")

    def apply(self, func):
        self.assert_domain_valid(self.args, self.domain)
        result = func(**self)
        self.assert_codomain_valid(result, self.codomain)
        return result

    def __copy__(self):
        return type(self)(self.args, self.keywords, self.domain, self.codomain)



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
        self.codomain = tuple()

    def __rshift__(self, mapping):
        codomain = getattr(mapping, 'codomain', mapping)
        return Arrow(self.domain, codomain)

class Codomain(Mapping):
    def __init__(self, codomain):
        self.domain = tuple()
        self.codomain = codomain


