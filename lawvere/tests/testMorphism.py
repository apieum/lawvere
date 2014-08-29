# -*- coding: utf-8 -*-
from lawvere import Morphism, morphism
from . import testCurry
from sys import version_info
if version_info >= (3, ):
    from .morphism3 import Morphism3Test


def annotate(func):
    setattr(func, '__annotations__', {'a': int, 'b': int, 'return': int})
    return func

class MorphismTest(testCurry.CurryTest):
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
        add.check_domain = True
        with self.assertRaises(TypeError):
            add(4, 2)

    def test_it_raises_type_error_if_args_not_instance_of_domain(self):
        morph = morphism((str, int), int)
        add = morph(lambda x, y: x + y)
        add.check_domain = True
        with self.assertRaises(TypeError):
            add(4, 2)

    def test_it_raises_type_error_if_result_not_instance_of_codomain(self):
        morph = morphism((int, int), str)
        add = morph(lambda x, y: x + y)
        add.check_codomain = True
        with self.assertRaises(TypeError):
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
        with self.assertRaises(TypeError):
            add(1) >> concat

    def test_it_checks_partial_args_to_compose(self):
        morph1 = morphism((int, int), int)
        morph2 = morphism((int, str), str)
        add = morph1(lambda x, y: x + y)
        cast_concat = morph2(lambda s1, s2: str(s1) + s2)
        with self.assertRaises(TypeError):
            add(1) >> cast_concat(1)

    def test_it_checks_stacks_to_pipe(self):
        morph1 = morphism((int, int), int)
        morph2 = morphism((str, str), str)
        add = morph1(lambda x, y: x + y)
        add2 = add(1) >> add(1)
        concat = morph2(lambda s1, s2: s1 + s2)
        with self.assertRaises(TypeError):
            add2 >> concat('text')

    def test_it_checks_stacks_to_circle(self):
        morph1 = morphism((int, int), int)
        morph2 = morphism((str, str), str)
        add = morph1(lambda x, y: x + y)
        add2 = add(1) >> add(1)
        concat = morph2(lambda s1, s2: s1 + s2)
        with self.assertRaises(TypeError):
            add2 << concat('text')

    def test_accept_is_false_if_an_arg_is_not_of_the_good_type(self):
        expected = self.Type(self.expected)
        self.assertFalse(expected.accept(('1', )))

    def test_accept_is_false_if_an_kwarg_is_not_of_the_good_type(self):
        expected = self.Type(self.expected)
        self.assertFalse(expected.accept(kwargs={'b':'1'}))


    def test_can_disable_domain_check(self):
        morph = morphism((int, int), str)
        add = morph(lambda x, y: x + y)
        with self.assertRaises(TypeError):
            add('a', 'b')
        add.checking(False)
        self.assertEqual('ab', add('a', 'b'))


    def test_can_disable_codomain_check(self):
        morph = morphism((int, int), str)
        add = morph(lambda x, y: x + y)
        with self.assertRaises(TypeError):
            add(1, 2)

        add.checking(False)
        self.assertEqual(3, add(1, 2))

    def test_when_calling_stack_first_item_domain_is_checked(self):
        morph = morphism((int, int), int)
        add = morph(lambda x, y: x + y)
        add2 = add(1) >> add(1)
        with self.assertRaises(TypeError) as context:
            add2('n')
        self.assertIn(' domain', str(context.exception))
        self.assertFalse(add2[0].check_domain)

    def test_when_calling_stack_last_item_codomain_is_checked(self):
        morph = morphism(int, int)
        identity = morph(lambda x: x)
        tostr = morph(lambda x: "%s" %x)
        inttostr = identity >> tostr
        with self.assertRaises(TypeError) as context:
            inttostr(1)
        self.assertIn(' codomain', str(context.exception))
        self.assertFalse(inttostr[0].check_domain)

    def test_when_replacing_at_it_checks_if_composable(self):
        morph1 = morphism(int, int)
        morph2 = morphism(int, str)
        identity = morph1(lambda x: x)
        tostr = morph2(lambda x: "%s" %x)
        inttostr = identity >> tostr
        with self.assertRaises(TypeError) as context:
            inttostr.replace_at(0, tostr)
        self.assertIn('Cannot compose', str(context.exception))

    def test_when_replacing_it_checks_if_composable(self):
        morph1 = morphism(int, int)
        morph2 = morphism(int, str)
        identity = morph1(lambda x: x)
        tostr = morph2(lambda x: "%s" %x)
        inttostr = tostr << identity
        with self.assertRaises(TypeError) as context:
            inttostr.replace(identity, identity >> tostr)
        self.assertIn('Cannot compose', str(context.exception))

    def test_when_only_one_item_it_checks_domain_and_codomain(self):
        morph = morphism(int, int)
        identity = morph(lambda x: x)
        tostr = morph(lambda x: "%s" %x)
        # create stack and enforce 'without' testing
        inttostr = (identity >> tostr).without(identity)
        with self.assertRaises(TypeError) as context:
            inttostr('1')
        self.assertIn(' domain', str(context.exception))
        with self.assertRaises(TypeError) as context:
            inttostr(1)
        self.assertIn(' codomain', str(context.exception))
