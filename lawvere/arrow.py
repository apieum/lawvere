# -*- coding: utf-8 -*-

Default = type('Default', (tuple, ), {})()

def Arrow(domain=Default, codomain=Default, func_type=lambda func: func):
    if type(domain) == type:
        domain = (domain, )

    if callable(domain):
        return func_type(domain)

    def call(func):
        varnames = getattr(func.__code__, 'co_varnames', tuple())
        annotations = getattr(func, '__annotations__', {})
        annotations.update(zip(varnames, domain))
        if codomain is not Default:
            annotations['return'] = codomain
        setattr(func, '__annotations__', annotations)
        return func_type(func)
    return call

def ArrowType(cls):
    return lambda domain=Default, codomain=Default: Arrow(domain, codomain, cls)
