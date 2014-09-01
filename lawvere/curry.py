# -*- coding: utf-8 -*-
from .signatures import from_func
from .stack import composable


@composable
class Curry(object):
    def __init__(self, func, signature=None):
        self.func = func
        self.signature = signature or from_func(type(self).__name__, func)

    @property
    def __name__(self):
        return self.func.__name__

    @property
    def __annotations__(self):
        return self.signature.annotations

    def with_default(self, *args, **kwargs):
        return type(self)(self.func, self.signature.merge(*args, **kwargs))

    def __call__(self, *args, **kwargs):
        signature = self.signature.merge(*args, **kwargs)
        if signature.valid():
            return self.apply(signature)

        return type(self)(self.func, signature)

    def __eq__(self, other):
        return self.func == other.func and self.signature == other.signature

    def apply(self, signature):
        return self.func(**signature)

    def accept(self, args=tuple(), kwargs=dict()):
        args_check = len(args) <= self.signature.argcount
        kwargs_check = set(kwargs.keys()).issubset(set(self.signature.keys()))
        return  args_check and kwargs_check
