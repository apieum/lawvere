# -*- coding: utf-8 -*-
from unittest import TestCase


class DocExamples3Test(TestCase):
    def test_example1_quick_start3(self):
        from lawvere import arrow

        @arrow
        def add(x:int, y:int) -> int:
            return x + y

        # identical use as Python 2 #

        # Type Checking:
        type_checked = False
        try:
            add('a', 'b') == 'ab'
        except TypeError:
            type_checked = True

        assert type_checked, 'add should not exists for str types'

        # dispatch
        @add.register
        def concat(x:str, y:str) -> str:
            return "%s %s" %(x, y)

        assert concat('a', 'b') == 'a b'
        # now add exists for str types:
        assert add('a', 'b') == 'a b'

        # type is also checked when composing... see python 2 ex.




