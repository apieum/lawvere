# -*- coding: utf-8 -*-
from unittest import TestCase
from lawvere import morphism

class Morphism3Test(TestCase):
    def test_it_found_domain_and_codomain_with_annotations(self):
        @morphism()
        def add(x:int, y:int) -> int:
            return x + y

        self.assertEquals(add.domain, {'x':int, 'y':int})
        self.assertEquals(add.codomain, int)

    def test_it_overrides_annotations(self):
        @morphism(str, str)
        def add(x:int, y:int) -> int:
            return x + y

        self.assertEquals(add.domain, {'x':str, 'y':int})
        self.assertEquals(add.codomain, str)

    def test_it_can_be_called_as_a_decorator(self):
        @morphism
        def add(x:int, y:int) -> int:
            return x + y

        self.assertTrue(add.composable_with(add))
