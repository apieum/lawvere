# -*- coding: utf-8 -*-
from collections import OrderedDict
__all__=['Undefined', 'signature_factory', 'use_signature', 'Signature', 'from_func']

Undefined = type('Undefined', (object, ), {})
Void = type('Void', (object, ), {
    '__instancecheck__': lambda self, instance: instance==None,
    '__subclasscheck__': lambda self, subclass: subclass in (NoneType, Void)
})


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
    def __init__(self, args, kwargs, args_infos={}, return_infos=Void):
        self.argcount = len(args)
        OrderedDict.__init__(self, args)
        self.update(kwargs)
        self.args_infos = args_infos
        self.return_infos = return_infos

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
    def from_func(cls, func):
        defaults = func.__defaults__ or tuple()
        argcount = getattr(func.__code__, 'co_argcount') - len(defaults)
        varnames = getattr(func.__code__, 'co_varnames')
        args = OrderedDict.fromkeys(varnames[:argcount], Undefined)
        keywords = OrderedDict(zip(varnames[argcount:], defaults))

        annotations = dict(getattr(func,  '__annotations__', {}))
        return_infos = Void
        if 'return' in annotations:
            return_infos = annotations['return'] or Void
            del annotations['return']

        return cls(args, keywords, annotations, return_infos)

    def __copy__(self):
        return type(self)(self.args, self.keywords, self.args_infos, self.return_infos)

