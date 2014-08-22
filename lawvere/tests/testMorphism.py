# -*- coding: utf-8 -*-
from lawvere.morphism import Morphism, morphism

def Curry():
    from .testCurry import CurryTest
    return CurryTest

def annotate(func):
    setattr(func, '__annotations__', {'a': int, 'b': int, 'return': int})
    return func

class MorphismTest(Curry()):
    Type = Morphism
    @staticmethod
    @annotate
    def expected(a, b):
        pass

    @staticmethod
    @annotate
    def sub(a, b):
        return a - b

    @staticmethod
    @annotate
    def mul(a, b):
        return a * b


    def test_it_raises_type_error_if_domain_len_not_equals_args_len(self):
        morph = morphism(int, int)
        add = morph(lambda x, y: x + y)
        with self.assertRaises(TypeError) as context:
            add(4, 2)

    def test_it_raises_type_error_if_args_not_instance_of_domain(self):
        morph = morphism((str, int), int)
        add = morph(lambda x, y: x + y)
        with self.assertRaises(TypeError) as context:
            add(4, 2)

    def test_it_raises_type_error_if_result_not_instance_of_codomain(self):
        morph = morphism((int, int), str)
        add = morph(lambda x, y: x + y)
        with self.assertRaises(TypeError) as context:
            add(4, 2)

    def test_it_knows_if_is_composable_with_other_morphism(self):
        morph = morphism((int, int), int)
        add = morph(lambda x, y: x + y)
        self.assertTrue(add.composable_with(add))

    def test_it_raises_an_error_when_cannot_compose(self):
        morph1 = morphism((int, int), int)
        morph2 = morphism((str, str), str)
        add = morph1(lambda x, y: x + y)
        concat = morph2(lambda s1, s2: s1 + s2)
        with self.assertRaises(TypeError) as context:
            add(1) >> concat

    def test_it_checks_partial_args_to_compose(self):
        morph1 = morphism((int, int), int)
        morph2 = morphism((int, str), str)
        add = morph1(lambda x, y: x + y)
        cast_concat = morph2(lambda s1, s2: str(s1) + s2)
        with self.assertRaises(TypeError) as context:
            add(1) >> cast_concat(1)

    def test_it_checks_stacks_to_pipe(self):
        morph1 = morphism((int, int), int)
        morph2 = morphism((str, str), str)
        add = morph1(lambda x, y: x + y)
        add2 = add(1) >> add(1)
        concat = morph2(lambda s1, s2: s1 + s2)
        with self.assertRaises(TypeError) as context:
            add2 >> concat('text')

    def test_it_checks_stacks_to_circle(self):
        morph1 = morphism((int, int), int)
        morph2 = morphism((str, str), str)
        add = morph1(lambda x, y: x + y)
        add2 = add(1) >> add(1)
        concat = morph2(lambda s1, s2: s1 + s2)
        with self.assertRaises(TypeError) as context:
            add2 << concat('text')

