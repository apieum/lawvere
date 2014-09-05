# -*- coding: utf-8 -*-
from unittest import TestCase

from sys import version_info
if version_info >= (3, ):
    from .doc3 import DocExamples3Test

class DocExamplesTest(TestCase):
    def test_example1_quick_start(self):
        from lawvere import arrow

        # first argument is a tuple of types called "domain" (args type)
        # second argument is called "codomain" (return type)
        @arrow((int, int), int)
        def add(x, y):
            return x + y

        # currying:
        add2 = add(2)

        assert add2(3) == 5
        assert add(1)(2) == 3 # successive calls

        # composition (pipe):
        # pass the result of first function to second
        add4 = add2 >> add2
        assert add4(1) == 5
        # composition (circle):
        # pass result of add(1) into add4
        add5 = add4 << add(1)
        assert add5(5) == 10

        # composed functions are tuples:
        assert isinstance(add4, tuple)
        assert add5[1] == add4

        # equality is checked over signatures:
        assert add(1) == add(1)
        assert add5 == add(1) >> add2 >> add2

        # operator precedence:
        assert add5 == add(1) >> (add2 << add2)
        assert add5 == add2 >> add2 << add(1)

        # Type Checking:
        type_checked = False
        try:
            add('a', 'b') == 'ab'
        except TypeError:
            type_checked = True

        assert type_checked, 'add should not exists for str types'


        # dispatch register
        # concat inherit arrow properties
        @add.register((str, str), str)
        def concat(x, y):
            return "%s %s" %(x, y)

        # can still call/curry... concat
        assert concat('a')('b') == 'a b'
        # add with str call concat
        assert add('a') == concat('a')

        # Concat is only defined for str
        type_checked = False
        try:
            assert concat(1, 2) == 3
        except TypeError:
            type_checked = True

        assert type_checked, 'concat should not exists for int types'

        # Type Checking when composing:
        try:
            add >> concat(y='b')
        except TypeError as exc:
            message = str(exc)
        # hope message is clear :)
        assert message == "Cannot compose add -> int with concat(x:str=Undefined, y:str=b)"
        # if composition was circle message would be:
        # ... concat -> str with add(x:int=Undefined, y:int=Undefined)



