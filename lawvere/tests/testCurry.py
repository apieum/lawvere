# -*- coding: utf-8 -*-
from unittest import TestCase
from lawvere.curry import Curry


class CurryTest(TestCase):
    def test_it_doesnt_support_builtins_functions(self):
        with self.assertRaises(TypeError):
            curry = Curry(next)

    def test_it_has_given_userdefined_func_name(self):
        def expected(a, b):
            pass
        curry = Curry(expected)
        self.assertEqual('expected', curry.__name__)

    def test_it_make_callable_partial(self):
        @Curry
        def sub(a, b):
            return a - b
        self.assertEqual(4, sub(7)(3))
        self.assertEqual(4, sub(b=3)(7))

    def test_it_permits_composition_with_g_after_f(self):
        @Curry
        def sub(a, b):
            return a - b

        @Curry
        def mul(a, b):
            return a * b

        mul2_of_sub3 = mul(2) << sub(b=3)
        self.assertEqual(4, mul2_of_sub3(5))

    def test_it_permits_composition_with_f_before_g(self):
        @Curry
        def sub(a, b):
            return a - b

        @Curry
        def mul(a, b):
            return a * b

        mul2_before_sub3 = mul(2) >> sub(b=3)
        self.assertEqual(7, mul2_before_sub3(5))

    def test_it_composed_func_can_be_managed_as_list(self):
        @Curry
        def sub(a, b):
            return a - b
        @Curry
        def mul(a, b):
            return a * b

        mul2_before_sub3 = mul(2) >> sub(b=3)
        self.assertEqual(sub(b=3), mul2_before_sub3[1])
        self.assertEqual(mul(2), mul2_before_sub3[0])
        self.assertEqual(7, mul2_before_sub3(5))

    def test_it_can_del_stack_item(self):
        @Curry
        def sub(a, b):
            return a - b
        @Curry
        def mul(a, b):
            return a * b

        mul2_before_sub3 = mul(2) >> sub(b=3)
        sub3 = mul2_before_sub3.without(mul(2))
        self.assertEqual(sub(b=3), sub3)
        mul2 = mul2_before_sub3.without(sub3)
        self.assertEqual(mul(2), mul2)

    def test_it_can_replace_stack_item_at_key(self):
        @Curry
        def sub(a, b):
            return a - b
        @Curry
        def mul(a, b):
            return a * b

        mul2_of_sub3 = mul(2) << sub(b=3)
        mul2_of_sub2 = mul2_of_sub3.replace_at(0, sub(b=2))
        self.assertEqual(6, mul2_of_sub2(5))

        mul3_of_sub3 = mul2_of_sub3.replace_at(1, mul(3))
        self.assertEqual(6, mul3_of_sub3(5))

    def test_it_can_replace_stack_item(self):
        @Curry
        def sub(a, b):
            return a - b
        @Curry
        def mul(a, b):
            return a * b

        mul2_of_sub3 = mul(2) << sub(b=3)
        mul2_of_sub2 = mul2_of_sub3.replace(sub(b=3), sub(b=2))
        self.assertEqual(6, mul2_of_sub2(5))

        mul3_of_sub3 = mul2_of_sub3.replace(mul(2), mul(3))
        self.assertEqual(6, mul3_of_sub3(5))


    def test_it_is_compared_over_values(self):
        sub = lambda a, b: a - b
        mul = lambda a, b: a * b

        self.assertEqual(Curry(sub), Curry(sub))
        self.assertNotEqual(Curry(sub)(1), Curry(sub))

        expected = Curry(mul)(2) >> Curry(sub)(b=3)
        self.assertEqual(Curry(mul)(2) >> Curry(sub)(b=3), expected)


    def test_it_returns_a_curry_when_all_args_not_given_with_before(self):
        @Curry
        def sub(a, b):
            return a - b
        @Curry
        def mul(a, b):
            return a * b

        curry = mul(2) >> mul >> sub(b=3)
        self.assertEqual(curry(3)(2), 9)

    def test_it_returns_a_curry_when_all_args_not_given_with_after(self):
        @Curry
        def sub(a, b):
            return a - b
        @Curry
        def mul(a, b):
            return a * b

        curry = sub(b=3) << mul << mul(2)
        self.assertEqual(curry(3)(2), 9)

