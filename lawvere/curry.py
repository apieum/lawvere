# -*- coding: utf-8 -*-
from .signatures import from_func
from .stack import composable


@composable
class Curry(object):
    def __init__(self, func, signature=None):
        self.func = func
        self.signature = signature

    @property
    def __name__(self):
        return self.func.__name__

    def __call__(self, *args, **kwargs):
        sig = self.update_signature(*args, **kwargs)
        if sig.defined():
            return sig.apply(self.func)

        return type(self)(self.func, signature=sig)

    def __eq__(self, other):
        return self.func == other.func and self.signature == other.signature

    def update_signature(self, *args, **kwargs):
        signature = self.signature or from_func(self, self.func)
        return signature.merge(*args, **kwargs)
