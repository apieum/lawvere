# -*- coding: utf-8 -*-
from unittest import TestCase
from lawvere.morphism import Morphism
from lawvere.mappings import Arrow

class MorphismTest(TestCase):
    def test_it_can_curry(self):
        morph = Arrow(int, int)
        func = lambda x, y=1, z=2: x + y + z
        morph = morph(func)
        add_5 = morph(z=3, y=2)
        self.assertEqual(10, add_5(5))

    def test_it_is_composable(self):
        morph = Arrow((int, int), int)
        add = morph(lambda x, y: x + y)
        sub = morph(lambda x, y: x - y)
        add_5_sub_2 = add(5) >> sub(y=2)
        self.assertEqual(10, add_5_sub_2(7))

    def test_it_raises_type_error_if_domain_len_not_equals_args_len(self):
        morph = Arrow(int, int)
        add = morph(lambda x, y: x + y)
        with self.assertRaises(TypeError) as context:
            add(4, 2)

    def test_it_raises_type_error_if_args_not_instance_of_domain(self):
        morph = Arrow((str, int), int)
        add = morph(lambda x, y: x + y)
        with self.assertRaises(TypeError) as context:
            add(4, 2)

    def test_it_raises_type_error_if_result_not_instance_of_codomain(self):
        morph = Arrow((int, int), str)
        add = morph(lambda x, y: x + y)
        with self.assertRaises(TypeError) as context:
            add(4, 2)

    def test_it_knows_if_is_composable_with_other_morphism(self):
        morph = Arrow((int, int), int)
        add = morph(lambda x, y: x + y)
        self.assertTrue(add.can_circle_with(add))
        self.assertTrue(add.can_pipe_with(add))
