# -*- coding: utf-8 -*-
from collections import OrderedDict
__all__=['Undefined', 'signature_factory', 'use_signature', 'Signature', 'from_func']

Undefined = type('Undefined', (object, ), {})

call = lambda self, wrapper, *args, **kwargs: self.get(type(wrapper).__name__, Signature)(*args, **kwargs)
signature_factory = type('SignatureFactory', (dict, ), {'__call__': call})()


def use_signature(sig):
    def set_signature(cls):
        signature_factory[type(cls).__name__] = sig
        return cls
    return set_signature


def from_func(wrapper, func):
    argcount = getattr(func.__code__, 'co_argcount', 0)
    defaults = func.__defaults__ or tuple()
    arglen = argcount - len(defaults)
    varnames = getattr(func.__code__, 'co_varnames', tuple())[:argcount]

    parameters = OrderedDict.fromkeys(varnames[:arglen], Undefined)
    parameters.update(zip(varnames[arglen:], defaults))
    return signature_factory(wrapper, parameters, arglen)


class Signature(OrderedDict):
    def __init__(self, parameters, argcount=0):
        OrderedDict.__init__(self, parameters)
        self.argcount = argcount

    def defined(self):
        return Undefined not in self.values()

    def merge(self, *args, **kwargs):
        binded = type(self)(self, self.argcount)
        binded.update(kwargs)
        binded.update(zip(binded.iter_undefined(), args))
        return binded

    def iter_undefined(self):
        index = 0
        for name, value in self.items():
            if value == Undefined or index >= self.argcount:
                yield name
            index+=1

    def apply(self, func):
        return func(**self)
