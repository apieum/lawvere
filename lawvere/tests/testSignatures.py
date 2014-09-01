# -*- coding: utf-8 -*-
from unittest import TestCase
from lawvere.signatures import from_func, Signature, Undefined


class SignatureTest(TestCase):
    def test_it_contains_all_args(self):
        def expected(a, b, c=""):
            pass
        sig = from_func('sigtype', expected)
        self.assertEqual(('a', 'b', 'c'), tuple(sig))

    def test_args_are_undefined_and_kwargs_have_value(self):
        def expected(a, b="expected"):
            pass
        sig = from_func('sigtype', expected)
        self.assertEqual(sig['a'], Undefined)
        self.assertEqual(sig['b'], "expected")

    def test_it_knows_if_args_are_defined(self):
        def expected(a, b="expected"):
            pass
        sig = from_func('sigtype', expected)
        self.assertFalse(sig.valid())
        sig['a'] = None
        self.assertTrue(sig.valid())


    def test_merge_returns_Signature_copy(self):
        sig = from_func('sigtype', lambda a, b, c=1: None)
        merge = sig.merge()
        self.assertIsInstance(merge, Signature)
        self.assertIsNot(sig, merge)
        self.assertEqual(sig, merge)

    def test_Signature_copy_add_values_to_arguments(self):
        sig = from_func('sigtype', lambda a, b, c=1: None)
        binded = sig.merge(1, c=3, b=2)
        self.assertEqual(binded['a'], 1)
        self.assertEqual(binded['b'], 2)
        self.assertEqual(binded['c'], 3)





