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
        if not item2.composable_with(item1):
            raise TypeError('Cannot compose %s -> %s with %s' %(item2.__name__, item2.codomain.__name__, repr(item1)))
        return cls(item1 + item2)


@compose_with(MorphismStack)
class Morphism(Curry):
    @property
    def domain(self):
        return self.signature.args_infos
    @property
    def codomain(self):
        return self.signature.return_infos

    def composable_with(self, other):
        arg_name = next(self.signature.iter_undefined())
        return issubclass(other.codomain, self.domain[arg_name])

    def __repr__(self):
        items = list()
        for name, item in self.signature.items():
            item = type(item) == type and item.__name__ or item
            items.append("%s:%s=%s" % (name, self.domain[name].__name__, item))
        return self.__name__ + ', '.join(items)

    def assert_domain_valid(self, args, domain):
        if len(args) != len(domain):
            raise TypeError("Domain not valid")
        for name, arg in args:
            if not isinstance(arg, domain[name]):
                raise TypeError("Argument %s not in domain" % name)

    def assert_codomain_valid(self, result, codomain):
        if not isinstance(result, codomain):
            raise TypeError("Result not in codomain")
        return result


    def apply(self, signature):
        self.assert_domain_valid(signature.args, self.domain)
        return self.assert_codomain_valid(self.func(**signature), self.codomain)

morphism = ArrowType(Morphism)
