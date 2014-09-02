# -*- coding: utf-8 -*-
from unittest import TestCase


class DocExamplesTest(TestCase):
    def test_example1_quick_start(self):
        from lawvere import arrow, typedef

        # explicit use of keywords only for meaning exposal
        @arrow(domain=(int, int), codomain=int)
        def add(x, y):
            return x + y

        # currying:
        add2 = add(2)

        assert add2(3) == 5
        assert add2(3) != 4, 'obviously: 2+3 != 4'

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

        # dispatch
        @add.register((str, str), str)
        def concat(x, y):
            return "%s%s" %(x, y)

        assert concat('a', 'b') == 'ab'
        assert add('a', 'b') == 'ab'



