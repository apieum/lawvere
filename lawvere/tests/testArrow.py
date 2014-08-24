# -*- coding: utf-8 -*-
from unittest import TestCase
from lawvere.arrow import Arrow

class ArrowTest(TestCase):
    def test_Arrow_is_a_decorator(self):
        self.assertTrue(callable(Arrow('dom', 'cod')))

    def test_Arrow_add_domain_and_codomain_in_func_annotations(self):
        @Arrow(domain=('source', ), codomain='target')
        def func(a):
            pass
        self.assertEqual('source', func.__annotations__['a'])
        self.assertEqual('target', func.__annotations__['return'])

    def test_Arrow_can_be_called_without_argument(self):
        def func(a):
            pass
        self.assertIs(Arrow(func), func)
