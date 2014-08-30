# -*- coding: utf-8 -*-
from .curry import Curry
Default = type('Default', (tuple, ), {})()

@Curry
def annotate(domain, codomain, func):
    varnames = getattr(func.__code__, 'co_varnames', tuple())
    annotations = getattr(func, '__annotations__', {})
    annotations.update(zip(varnames, domain))
    if codomain is not Default:
        annotations['return'] = codomain
    setattr(func, '__annotations__', annotations)
    return func


@Curry
def Arrow(domain, codomain=Default, func_type=lambda func: func):
    if type(domain) == type:
        domain = (domain, )

    if callable(domain):
        return func_type(domain)

    return lambda func: func_type(annotate(domain, codomain)(func))




def ArrowType(cls):
    return Arrow(func_type=cls)
