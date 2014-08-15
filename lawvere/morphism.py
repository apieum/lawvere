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
    @property
    def domain(self):
        return self.signature.domain
    @property
    def codomain(self):
        return self.signature.codomain

    def can_circle_with(self, other):
        return other.can_pipe_with(self)

    def can_pipe_with(self, other):
        return issubclass(self.codomain, other.domain[0])
