# -*- coding: utf-8 -*-
from collections import OrderedDict
__all__=['Undefined', 'signature_factory', 'use_signature', 'Signature', 'from_func']

Undefined = type('Undefined', (object, ), {})

call = lambda self, wrapper: self.get(type(wrapper).__name__, Signature)
signature_factory = type('SignatureFactory', (dict, ), {'__call__': call})()

def use_signature(signature):
    def set_signature(cls):
        signature_factory[cls.__name__] = signature
        return cls
    return set_signature


def from_func(wrapper, func):
    return signature_factory(wrapper).from_func(func)


class Signature(OrderedDict):
    def __init__(self, args, kwargs):
        self.argcount = len(args)
        OrderedDict.__init__(self, args)
        self.update(kwargs)

    @property
    def args(self):
        return tuple(self.items())[:self.argcount]

    @property
    def keywords(self):
        return tuple(self.items())[self.argcount:]

    def valid(self):
        return Undefined not in self.values()

    def merge(self, *args, **kwargs):
        signature = self.__copy__()
        signature.update(kwargs)
        signature.update(zip(signature.iter_settable(), args))
        return signature

    def iter_undefined(self):
        keys = tuple(self.keys())[:self.argcount]
        return iter(filter(lambda name: self[name] == Undefined, keys))

    def keywords_names(self):
        return tuple(self.keys())[self.argcount:]

    def iter_settable(self):
        return iter(tuple(self.iter_undefined()) + self.keywords_names())


    @classmethod
    def inspect_parameters(cls, func):
        argcount = getattr(func.__code__, 'co_argcount', 0)
        defaults = func.__defaults__ or tuple()
        arglen = argcount - len(defaults)
        varnames = getattr(func.__code__, 'co_varnames', tuple())[:argcount]

        args = OrderedDict.fromkeys(varnames[:arglen], Undefined)
        keywords = OrderedDict(zip(varnames[arglen:], defaults))
        return args, keywords

    @classmethod
    def from_func(cls, func):
        return cls(*cls.inspect_parameters(func))

    def __copy__(self):
        return type(self)(self.args, self.keywords)
