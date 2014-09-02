# -*- coding: utf-8 -*-
from collections import OrderedDict
__all__=['Undefined', 'signature_factory', 'use_signature', 'Signature', 'from_func']

Undefined = type('Undefined', (type, ), {})


call = lambda self, sigtype: self.get(sigtype, Signature)
signature_factory = type('SignatureFactory', (dict, ), {'__call__': call})()

def use_signature(signature):
    def set_signature(cls):
        signature_factory[cls.__name__] = signature
        return cls
    return set_signature


def from_func(sigtype, func):
    return signature_factory(sigtype).from_func(func)

typename = lambda item: type(item) == type and item.__name__ or item

class Annotations(dict):
    def returns(self):
        return self.get('return', None)

    def args(self):
        args = dict(self)
        args.pop('return')
        return args

    def __setitem__(self, name, value):
        raise ValueError('Cannot set Annotations items')


class Signature(OrderedDict):
    def __init__(self, args, kwargs, annotations=Annotations()):
        self.argcount = len(args)
        OrderedDict.__init__(self, args)
        self.update(kwargs)
        self.annotations = annotations

    def arg_info(self, name):
        return "%s:%s=%s" % (name, typename(self.annotations[name]), typename(self[name]))

    @property
    def args_infos(self):
        return ', '.join([self.arg_info(name) for name in self.keys()])

    @property
    def return_infos(self):
        return '-> %s' %typename(self.return_annotation)

    @property
    def return_annotation(self):
        return self.annotations.returns()
    @property
    def args_annotation(self):
        return self.annotations.args()

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
        return iter(name for name in self.args_names() if self[name] == Undefined)

    def iter_defined(self):
        return iter(name for name in self.args_names() if self[name] != Undefined)

    def args_names(self):
        keys = iter(self)
        for i in range(self.argcount):
            yield next(keys)

    def keywords_names(self):
        return tuple(self.keys())[self.argcount:]

    def iter_settable(self):
        return tuple(self.iter_undefined()) + self.keywords_names()

    @classmethod
    def from_func(cls, func):
        if hasattr(func, 'signature'):
            return func.signature.__copy__()
        defaults = func.__defaults__ or tuple()
        argcount = getattr(func.__code__, 'co_argcount') - len(defaults)
        varnames = getattr(func.__code__, 'co_varnames')
        args = OrderedDict.fromkeys(varnames[:argcount], Undefined)
        keywords = OrderedDict(zip(varnames[argcount:], defaults))

        annotations = Annotations(getattr(func,  '__annotations__', {}))

        return cls(args, keywords, annotations)

    def __copy__(self):
        return type(self)(self.args, self.keywords, self.annotations)
