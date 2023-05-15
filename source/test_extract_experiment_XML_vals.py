#!/usr/bin/env python3
"""Some simple tests of the SRA_EXPERIMENT_SPEC main used methods in the extract_experiment_XML_vals.py
   The tested methods are those currently used in ExperimentChecklists2Json.py

___author___ = "woollard@ebi.ac.uk"
___start_date___ = 2023-05-15
__docformat___ = 'reStructuredText'

"""

import unittest
from icecream import ic
#ic.disable()
import sys
from attr import define

import ExperimentChecklists2Json
from extract_experiment_XML_vals import *

class TestSRA_EXPERIMENT_SPEC(unittest.TestCase):

    def setUp(self):
        self.sra_obj = get_SRA_XML_baseline()
        # print(self.sra_obj.common_schema_level)
        # print(self.sra_obj.get_library_strategy_list())
        # print(self.sra_obj.get_targetted_loci_list())

    def tearDown(self):
        ic()

    def test_get_library_strategy_list(self):
         print("test_get_library_strategy_list")
         self.assertTrue(len(self.sra_obj.get_library_strategy_list()) > 5)

    def test_get_targetted_loci_list(self):
        print("test_get_targetted_loci_list")
        test_val = ['16S rRNA', '18S rRNA', '28S rRNA', 'COX1', 'ITS1-5.8S-ITS2', 'RBCL', 'exome', 'matK', 'other']
        self.assertEqual(self.sra_obj.get_targetted_loci_list(), test_val)

    def test_get_library_source_list(self):
        print("test get_library_source_list")
        self.assertTrue(len(self.sra_obj.get_library_source_list()) > 5)

    def test_get_instrument_list(self):
        print("test get_instrument_list")
        self.assertTrue(len(self.sra_obj.get_instrument_list()) > 5)

    def test_get_platform_list(self):
        print("test get_platform_list")
        self.assertTrue(len(self.sra_obj.get_platform_list()) > 5)


if __name__ == '__main__':
    print("do some testing")
    ic.disable()
    unittest.main()

