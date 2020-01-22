# -*- coding: utf-8 -*-
from unittest import TestCase
from hexameterchecker import HexameterChecker, s, l, hexameter

__author__ = 'Bárdos Dávid'


class TestHexameterChecker(TestCase):
    def test_split_to_syllabes(self):
        h = HexameterChecker()
        result = h.split_to_pseudosyllabes("alma a fa alatt")
        self.assertEqual(["ALM", "A", "AF", "A", "AL", "ATT"], result)

    def test_get_length(self):
        h = HexameterChecker()
        self.assertEqual(l, h.get_length("ÚT"))
        self.assertEqual(l, h.get_length("ITT"))
        self.assertEqual(l, h.get_length("ITSZ"))
        self.assertEqual(s, h.get_length("A"))
        self.assertEqual(s, h.get_length("AZ"))
        self.assertEqual(s, h.get_length("ICS"))
        self.assertEqual(s, h.get_length("IDZ"))
        self.assertEqual(s, h.get_length("IDZS"))

    def test_check_line(self):
        sample = "Mért legyek én tisztességes? Kiterítenek úgyis!"
        # expected_result = "lss" + "ll" + "ll" + "lss" + "lss" + "ls"
        h = HexameterChecker()
        result = h.check_line(sample)
        self.assertEqual(hexameter, result)
