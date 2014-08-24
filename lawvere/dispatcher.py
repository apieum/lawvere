# -*- coding: utf-8 -*-

def dispatch(wrapper):
    def dispatch(func):
        func = FuncDispatch(func, wrapper)
        setattr(func[0], 'register', func.register)
        return func[0]
    return dispatch


class FuncDispatch(list):
    def __init__(self, func, wrapper):
        self.wrapper = wrapper
        self.func_ids = tuple()
        self.register(func)

    def __call__(self, *args, **kwargs):
        return DispatchResolver(self, args, kwargs)()

    def register(self, func):
        if id(func) not in self.func_ids:
            self.func_ids+= (id(func), )
            self.append(self.wrapper(func))
        return self


class DispatchResolver(list):
    def __init__(self, items, args, kwargs):
        list.__init__(self, items)
        self.args = args
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        args = self.args + args
        kwargs.update(self.kwargs)
        items = tuple(filter(lambda item: item.accept(args, kwargs), self))
        items_len = len(items)
        if  items_len == 1:
            return items[0](*args, **kwargs)
        if items_len > 1:
            return DispatchResolver(items, args, kwargs)

        raise ValueError('Given args have no corresponding function')

