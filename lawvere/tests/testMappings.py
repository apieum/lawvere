# -*- coding: utf-8 -*-
from unittest import TestCase
from lawvere.mappings import Arrow

class MappingsTest(TestCase):
    def test_Arrow_join_a_domain_and_a_codomain(self):
        arrow = Arrow(domain='Src', codomain='Trg')
        self.assertEqual('Src', arrow.domain)
        self.assertEqual('Trg', arrow.codomain)

    def test_mappings_are_decorators(self):
        self.assertTrue(callable(Arrow('dom', 'cod')))
