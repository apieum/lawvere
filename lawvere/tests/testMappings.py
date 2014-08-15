# -*- coding: utf-8 -*-
from unittest import TestCase
from lawvere.mappings import Mapping, Arrow, Domain, Codomain
from lawvere.morphism import Morphism

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
