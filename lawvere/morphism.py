# -*- coding: utf-8 -*-
from .curry import Curry
from .stack import Stack, compose_with, compose_with_self
from .mappings import ArrowType

@compose_with_self
class MorphismStack(Stack):
    @classmethod
    def from_items(cls, item1, item2):
        item1 = cls.from_vartype(item1)
        item2 = cls.from_vartype(item2)
        if not item2.composable_with(item1):
            raise TypeError('Cannot compose %s with %s' %(item2.return_infos, item1.args_infos))
        return cls(item1 + item2)


@compose_with(MorphismStack)
class Morphism(Curry):
    @property
    def domain(self):
        return self.signature.args_annotation
    @property
    def codomain(self):
        return self.signature.return_annotation

    @property
    def args_infos(self):
        return '%s%s' %(self.__name__, self.signature.args_infos)

    @property
    def return_infos(self):
        return '%s -> %s' %(self.__name__, self.signature.return_infos)

    def composable_with(self, other):
        arg_name = next(self.signature.iter_undefined())
        return issubclass(other.codomain, self.domain[arg_name])

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
