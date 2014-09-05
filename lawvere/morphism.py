# -*- coding: utf-8 -*-
from .curry import Curry
from .stack import Stack, compose_with

class MorphismStack(Stack):
    def __new__(cls, values=tuple()):
        self = tuple.__new__(cls, values)
        self.checking(False)
        return self

    def checking(self, value=False):
        tuple(map(lambda item: item.checking(False), self))

    def iochecks(self, check=True):
        self[0].check_domain = check
        self[-1].check_codomain = check

    def __call__(self, *args, **kwargs):
        self.iochecks(True)
        try:
            result = Stack.__call__(self, *args, **kwargs)
        except:
            self.iochecks(False)
            raise
        else:
            self.iochecks(False)
            return result

    @property
    def codomain(self):
        return self[-1].codomain

    @property
    def return_infos(self):
        return self[-1].return_infos

    def composable_with(self, other):
        return len(other) == 0 \
            or len(self) == 0 \
            or self[0].composable_with(other)

    def __addstacks__(self, stack1, stack2):
        if not stack2.composable_with(stack1):
            raise TypeError('Cannot compose %s with %s' %(stack1.return_infos, stack2.args_infos))
        stack1.checking(False)
        stack2.checking(False)
        return Stack.__addstacks__(self, stack1, stack2)


@compose_with(MorphismStack)
class Morphism(Curry):
    check_domain = True
    check_codomain = True

    def checking(self, value=False):
        self.check_domain = value
        self.check_codomain = value

    @property
    def domain(self):
        return self.signature.args_annotation
    @property
    def codomain(self):
        return self.signature.return_annotation

    @property
    def args_infos(self):
        return '%s(%s)' %(self.__name__, self.signature.args_infos)

    @property
    def return_infos(self):
        return '%s %s' %(self.__name__, self.signature.return_infos)

    def composable_with(self, other):
        arg_name = next(self.signature.iter_undefined())
        return issubclass(other.codomain, self.domain[arg_name])

    def assert_domain_valid(self, args, domain):
        if len(args) != len(domain):
            raise TypeError("Domain %s not valid for args: %s" %(domain, args))
        for name, arg in args:
            if not isinstance(arg, domain[name]):
                raise TypeError("Argument %s not in domain" % name)

    def assert_codomain_valid(self, result, codomain):
        if not isinstance(result, codomain):
            raise TypeError("Result not in codomain")

    def apply(self, signature):
        if self.check_domain:
            self.assert_domain_valid(signature.args, self.domain)
        result = self.func(**signature)
        if self.check_codomain:
            self.assert_codomain_valid(result, self.codomain)
        return result

    def accept(self, args=tuple(), kwargs=dict()):
        if not Curry.accept(self, args, kwargs): return False
        signature = self.signature.merge(*args, **kwargs)
        for name in signature.iter_defined():
            if not isinstance(signature[name], self.domain[name]):
                return False

        return True
