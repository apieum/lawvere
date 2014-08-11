# -*- coding: utf-8 -*-
from .signatures import from_func
from .stack import composable


@composable
class Curry(object):
    def __init__(self, func, signature=None):
        self._assert_signed(func)
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

    @classmethod
    def _assert_signed(cls, func):
        if not hasattr(func, "__code__"):
            name = getattr(func, '__name__', 'unnammed')
            raise TypeError("Can't read function %s signature" % name)


