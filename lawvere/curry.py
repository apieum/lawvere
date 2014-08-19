# -*- coding: utf-8 -*-
from .signatures import from_func
from .stack import composable


@composable
class Curry(object):
    def __init__(self, func, signature=None):
        self.func = func
        self.signature = signature or from_func(self, self.func)

    @property
    def __name__(self):
        return self.func.__name__

    @property
    def __annotations__(self):
        return self.signature.annotations

    def __call__(self, *args, **kwargs):
        signature = self.signature.merge(*args, **kwargs)
        if signature.valid():
            return self.apply(signature)

        return type(self)(self.func, signature=signature)

    def __eq__(self, other):
        return self.func == other.func and self.signature == other.signature


    def apply(self, signature):
        return self.func(**signature)
