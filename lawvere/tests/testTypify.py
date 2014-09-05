# -*- coding: utf-8 -*-
from unittest import TestCase
from lawvere.typify import typed

class TypedTest(TestCase):
    def test_typed_is_a_decorator(self):
        self.assertTrue(callable(typed('dom', 'cod')))

    def test_typed_add_domain_and_codomain_in_func_annotations(self):
        @typed(domain=('source', ), codomain='target')
        def func(a):
            pass
        self.assertEqual('source', func.__annotations__['a'])
        self.assertEqual('target', func.__annotations__['return'])

    def test_typed_can_be_called_without_argument(self):
        def func(a):
            pass
        self.assertIs(typed(func), func)
