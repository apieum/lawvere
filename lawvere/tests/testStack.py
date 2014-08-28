# -*- coding: utf-8 -*-
from unittest import TestCase
from lawvere.stack import is_composable, composable, Stack

class ComposableTest(TestCase):
    def test_it_returns_Stack_when_composing_two_functions(self):
        @composable
        def func1(arg):
            pass

        @composable
        def func2(arg):
            pass

        self.assertIsInstance(func2 << func1, Stack)
        self.assertIsInstance(func1 >> func2, Stack)

    def test_it_can_compare_composed(self):
        func1 = composable(lambda arg: True)
        func2 = composable(lambda arg: False)

        self.assertEqual(func2 << func2 << func1, func1 >> func2 >> func2)

    def test_it_can_compose_callable_object(self):
        @composable
        class func(object):
            def __call__(self):
                pass
        func1 = func()
        func2 = func()

        self.assertEqual(func2 << func1, func1 >> func2)

    def test_it_calls_functions_with_previous_function_result(self):
        add1 = composable(lambda arg: arg + 1)
        sub1 = composable(lambda arg: arg - 1)
        op = add1 >> sub1 >> sub1

        self.assertEqual(op(1), 0)

    def test_it_returns_partial_for_object(self):
        @composable
        class func(object):
            def __call__(self, a):
                if hasattr(self, 'a'):
                    return self.a + a
                setattr(self, 'a', a)
                return self
        add1 = func()
        add2 = func()

        op = add1 << add2(2)
        add5 = op(3)

        self.assertEqual(add5(5), 10)
        self.assertTrue(is_composable(add5))

    def test_if_result_is_composable_it_returns_partial(self):
        addx = composable(lambda a: composable(lambda b: a + b))
        op = addx << addx(2)
        add5 = op(3)

        self.assertEqual(add5(5), 10)
        self.assertTrue(is_composable(add5))

    def test_it_can_remove_composable_item(self):
        true = composable(lambda a: a and True)
        false = composable(lambda a: a and False)

        test1 = true >> false
        test2 = test1.without(false)

        self.assertEqual(test1(True), False)
        self.assertEqual(test2, true)
        self.assertEqual(test2(True), True)

    def test_it_can_remove_function_item_with_circle(self):
        true_func = lambda a: a and True
        true = composable(true_func)
        false = composable(lambda a: a and False)

        test1 = true >> false
        test2 = false >> false
        test3 = true >> true
        test4 = test1 << test2 >> test3
        self.assertEqual(test1.without(true_func), false)
        self.assertEqual(test4.without(test1), test2 >> test3)

    def test_it_can_remove_function_item_with_pipe(self):
        true_func = lambda a: a and True
        true = composable(true_func)
        false = composable(lambda a: a and False)

        test1 = true >> false
        test2 = false >> false
        test3 = true >> true
        test4 = test1 >> test2 >> test3
        self.assertEqual(test1.without(true_func), false)
        self.assertEqual(test4.without(test2), test1 >> test3)


    def test_it_can_replace_composable_item(self):
        true = composable(lambda a: a and True)
        false = composable(lambda a: a and False)

        test1 = true >> false
        test2 = false >> false
        test3 = true >> true
        test4 = test1 >> test2 >> test3

        test5 = test4.replace(false, true)
        test6 = test4.replace(test1 >> test2, test3) >> test3

        self.assertEqual(test4(True), False)
        self.assertEqual(test5(True), True)
        self.assertEqual(test6, test5)

    def test_it_can_replace_item_at_index(self):
        true = composable(lambda a: a and True)
        false = composable(lambda a: a and False)

        test1 = true >> false
        expected = true >> true

        self.assertEqual(test1.replace_at(1, true), expected)
        self.assertEqual(test1.replace_at(1, true >> true), expected >> true)

    def test_it_returns_stacktype_when_slicing(self):
        true = composable(lambda a: a and True)
        false = composable(lambda a: a and False)
        test1 = true >> false
        self.assertIsInstance(test1[1:], Stack)




