# -*- coding: utf-8 -*-
from unittest import TestCase
from mock import Mock
from lawvere.dispatcher import Dispatcher


class DispatcherTest(TestCase):
    def test_it_is_callable_and_returns_a_func_with_register(self):
        given = self.dispatch(lambda func: func)
        self.assertTrue(callable(given))
        self.assertTrue(hasattr(given, 'register'))

    def test_it_call_wrapped_item_accept_method(self):
        expected = 'expected'
        item = self.item(True)
        self.dispatch(item)(expected)
        item.accept.assert_called_once_with((expected, ), {})

    def test_it_raises_TypeError_if_accept_is_false_for_all_items(self):
        expected = 'expected'
        item = self.item(False)
        with self.assertRaises(TypeError):
            self.dispatch(item)(expected)

    def test_it_call_item_if_one_found(self):
        expected = 'expected'
        item1 = self.item(False)
        item2 = self.item(True)
        self.dispatch(item1, item2)(expected)
        self.assertFalse(item1.called)
        item2.assert_called_once_with(expected)

    def test_it_returns_Dispatcher_if_more_than_one_item_found(self):
        expected = 'expected'
        item1 = self.item(True)
        item2 = self.item(False)
        item3 = self.item(True)
        result = self.dispatch(item1, item2, item3)(expected)
        self.assertIsInstance(result, Dispatcher)
        self.assertEqual([item1, item3], list(result))


    def item(self, accept=True, returns='expected'):
        item = Mock(return_value=returns)
        item.accept.return_value = accept
        return item

    def dispatch(self, *items):
        return Dispatcher(items)


