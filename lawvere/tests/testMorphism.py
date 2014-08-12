# -*- coding: utf-8 -*-
from unittest import TestCase
from lawvere.morphism import Morphism, Mapping, Arrow, Domain, Codomain

class MappingsTest(TestCase):
    def test_Arrow_join_a_domain_and_a_codomain(self):
        arrow = Arrow(domain='Src', codomain='Trg')
        self.assertEqual('Src', arrow.domain)
        self.assertEqual('Trg', arrow.codomain)

    def test_mappings_are_decorators(self):
        self.assertTrue(callable(Mapping()))

    def test_domain_rshift_codomain_returns_an_Arrow(self):
        arrow = Domain('dom') >> Codomain('cod')
        self.assertIsInstance(arrow, Arrow)

    def test_domain_rshift_value_returns_arrow_with_value_as_codomain(self):
        arrow = Domain('dom') >> 'cod'
        self.assertEqual('cod', arrow.codomain)
        self.assertEqual('dom', arrow.domain)

    def test_domain_rshift_codomain_returns_morphism_decorator(self):
        arrow = Domain('dom') >> Codomain('cod')
        @arrow
        def func(x):
            pass
        self.assertIsInstance(func, Morphism)


class MorphismTest(TestCase):
    def test_it_can_curry(self):
        func = lambda x, y=1, z=2: x + y + z
        morph = Morphism(func)
        add_5 = morph(z=3, y=2)
        self.assertEqual(10, add_5(5))

    def test_it_is_composable(self):
        add = Morphism(lambda x, y: x + y)
        sub = Morphism(lambda x, y: x - y)
        add_5_sub_2 = add(5) >> sub(y=2)
        self.assertEqual(10, add_5_sub_2(7))
