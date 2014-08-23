# -*- coding: utf-8 -*-
from unittest import TestCase
from mock import Mock
from lawvere.dispatcher import dispatch, FuncDispatch, DispatchResolver


class DispatchTest(TestCase):
    def test_it_is_callable_and_returns_a_FuncDispatch_when_calling(self):
        given = dispatch(lambda func: func)
        self.assertTrue(callable(given))
        self.assertIsInstance(given(lambda: None), FuncDispatch)

class FuncDispatchTest(TestCase):
    def test_it_registers_wrapper_results(self):
        given = self.dispatch("expected 0", wrapper=lambda func: "got %s" %func)
        self.assertEqual("got expected 0", given[0])
        given.register("expected 1")
        self.assertEqual("got expected 1", given[1])

    def test_it_call_wrapped_item_accept_method(self):
        expected = 'expected'
        item = self.item(True)
        self.dispatch(item)(expected)
        item.accept.assert_called_once_with((expected, ), {})

    def test_it_call_raise_error_if_accept_is_false_for_all_items(self):
        expected = 'expected'
        item = self.item(False)
        with self.assertRaises(ValueError) as context:
            self.dispatch(item)(expected)

    def test_it_call_item_if_one_found(self):
        expected = 'expected'
        item = self.item(True)
        self.dispatch(item)(expected)
        item.assert_called_once_with(expected)

    def test_it_returns_DispatchResolver_if_more_than_one_item_found(self):
        expected = 'expected'
        item1 = self.item(True)
        item2 = self.item(False)
        item3 = self.item(True)
        result = self.dispatch(item1, item2, item3)(expected)
        self.assertIsInstance(result, DispatchResolver)
        self.assertEqual([item1, item3], list(result))

    def item(self, accept=True, returns='expected'):
        item = Mock(return_value=returns)
        item.accept.return_value = accept
        return item

    def dispatch(self, item, *args, **kwargs):
        wrapper = kwargs.get('wrapper', lambda func: func)
        func = FuncDispatch(item, wrapper)
        for item in args:
            func.register(item)
        return func


