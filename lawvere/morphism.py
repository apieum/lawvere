# -*- coding: utf-8 -*-
from .curry import Curry
from .signatures import use_signature, Signature
from .stack import Stack, compose_with, compose_with_self
from .mappings import ArrowType

@compose_with_self
class MorphismStack(Stack):
    @classmethod
    def from_items(cls, item1, item2):
        item1 = cls.from_vartype(item1)
        item2 = cls.from_vartype(item2)
        if not item1.can_pipe_with(item2):
            raise TypeError('Cannot compose %s -> %s with %s%s' %(item1.__name__, item1.codomain.__name__, item2.__name__, repr(item2)))
        return cls(item1 + item2)

class MorphismSignature(Signature):
    def __init__(self, args, kwargs, domain=tuple(), codomain=tuple()):
        Signature.__init__(self, args, kwargs)
        self.domain = domain
        self.codomain = codomain

    @classmethod
    def from_func(cls, func):
        domain = getattr(func, 'domain', tuple())
        codomain = getattr(func, 'codomain', None)
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


@compose_with(MorphismStack)
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
        arg_name = next(other.signature.iter_undefined())
        arg_key = tuple(other.signature).index(arg_name)
        return issubclass(self.codomain, other.domain[arg_key])

    def __repr__(self):
        items = list()
        index = 0
        for name, item in self.signature.items():
            item = type(item) == type and item.__name__ or item
            items.append("%s:%s=%s" % (name, self.domain[index].__name__, item))
            index+=1
        return ', '.join(items)

morphism = ArrowType(Morphism)
