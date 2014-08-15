# -*- coding: utf-8 -*-
from .signatures import from_func
from .stack import composable


@composable
class Curry(object):
    def __init__(self, func, signature=None):
        self.func = func
        self.__dict__['signature'] = signature

    @property
    def signature(self):
        return self.__dict__['signature'] or from_func(self, self.func)

    @property
    def __name__(self):
        return self.func.__name__

    def __call__(self, *args, **kwargs):
        sig = self.signature.merge(*args, **kwargs)
        if sig.defined():
            return sig.apply(self.func)

        return type(self)(self.func, signature=sig)

    def __eq__(self, other):
        return self.func == other.func and self.signature == other.signature
