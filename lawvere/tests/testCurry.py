# -*- coding: utf-8 -*-
from unittest import TestCase
from lawvere import Curry


class CurryTest(TestCase):
    Type = Curry
    @staticmethod
    def expected(a, b):
        pass

    @staticmethod
    def sub(a, b):
        return a - b

    @staticmethod
    def mul(a, b):
        return a * b
    def test_it_has_given_userdefined_func_name(self):
        curry = self.Type(self.expected)
        self.assertEqual('expected', curry.__name__)

    def test_it_is_a_tuple_of_func(self):
        sub = self.Type(self.sub)
        sub2_before_sub3 = sub(2) >> sub(b=3)
        self.assertEqual(sub(2), sub2_before_sub3[0])
        self.assertEqual(sub(b=3), sub2_before_sub3[1])

    def test_it_makes_callables_partials(self):
        sub = self.Type(self.sub)
        self.assertEqual(4, sub(7)(3))
        self.assertEqual(4, sub(b=3)(7))

    def test_it_permits_composition_with_g_after_f(self):
        mul = self.Type(self.mul)
        sub = self.Type(self.sub)
        mul2_of_sub3 = mul(2) << sub(b=3)
        self.assertEqual(4, mul2_of_sub3(5))

    def test_it_permits_composition_with_f_before_g(self):
        mul = self.Type(self.mul)
        sub = self.Type(self.sub)

        mul2_before_sub3 = mul(2) >> sub(b=3)
        self.assertEqual(7, mul2_before_sub3(5))

    def test_it_can_del_stack_item(self):
        mul = self.Type(self.mul)
        sub = self.Type(self.sub)

        mul2_sub3 = mul(2) >> sub(b=3)
        self.assertEqual(sub(b=3), mul2_sub3.without(mul(2)))
        self.assertEqual(mul(2), mul2_sub3.without(sub(b=3)))

    def test_it_can_replace_stack_item_at_key(self):
        mul = self.Type(self.mul)
        sub = self.Type(self.sub)

        mul2_of_sub3 = mul(2) << sub(b=3)
        mul2_of_sub2 = mul2_of_sub3.replace_at(0, sub(b=2))
        self.assertEqual(6, mul2_of_sub2(5))

        mul3_of_sub3 = mul2_of_sub3.replace_at(1, mul(3))
        self.assertEqual(6, mul3_of_sub3(5))

    def test_it_can_replace_stack_item(self):
        mul = self.Type(self.mul)
        sub = self.Type(self.sub)

        mul2_of_sub3 = mul(2) << sub(b=3)
        mul2_of_sub2 = mul2_of_sub3.replace(sub(b=3), sub(b=2))
        self.assertEqual(6, mul2_of_sub2(5))

        mul3_of_sub3 = mul2_of_sub3.replace(mul(2), mul(3))
        self.assertEqual(6, mul3_of_sub3(5))


    def test_it_is_compared_over_values(self):
        self.assertEqual(self.Type(self.sub), self.Type(self.sub))
        self.assertNotEqual(self.Type(self.sub)(1), self.Type(self.sub))

        expected = self.Type(self.mul)(2) >> self.Type(self.sub)(b=3)
        self.assertEqual(self.Type(self.mul)(2) >> self.Type(self.sub)(b=3), expected)


    def test_it_returns_a_curry_when_all_args_not_given_with_before(self):
        mul = self.Type(self.mul)
        sub = self.Type(self.sub)

        curry = mul(2) >> mul >> sub(b=3)
        self.assertEqual(curry(3)(2), 9)

    def test_it_returns_a_curry_when_all_args_not_given_with_after(self):
        mul = self.Type(self.mul)
        sub = self.Type(self.sub)

        curry = sub(b=3) << mul << mul(2)
        self.assertEqual(curry(3)(2), 9)

    def test_it_accepts_args_if_count_is_lower_than_signature_require(self):
        expected = self.Type(self.expected)

        self.assertTrue(expected.accept((1, )))
        self.assertTrue(expected.accept((1, 2)))
        self.assertFalse(expected.accept((1, 2, 3)))


    def test_it_accepts_kwargs_if_keys_included_in_signature_keys(self):
        expected = self.Type(self.expected)

        self.assertTrue(expected.accept(kwargs={'a':1}))
        self.assertTrue(expected.accept(kwargs={'a':1, 'b':2}))
        self.assertFalse(expected.accept(kwargs={'c':1}))


