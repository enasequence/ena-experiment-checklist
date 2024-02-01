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
from SRA_EXPERIMENT_OBJ import *

class TestSRA_EXPERIMENT_SPEC(unittest.TestCase):

    def setUp(self):
        self.sra_obj = get_SRA_XML_baseline()
        # print(self.sra_obj.common_schema_level)
        # print(self.sra_obj.get_library_strategy_list())
        # print(self.sra_obj.get_targetted_loci_list())

    def tearDown(self):
        ic()

    def test_get_library_strategy_list(self):
        # print("test_get_library_strategy_list")
        # print(self.sra_obj.get_library_strategy_list())
        self.assertTrue(len(self.sra_obj.get_library_strategy_list()) > 5)
        self.assertTrue('WGS' in self.sra_obj.get_library_strategy_list())

    def test_get_targetted_loci_list(self):
        print("test_get_targetted_loci_list")
        ic(self.sra_obj.get_targetted_loci_list())
        self.assertTrue(len(self.sra_obj.get_targetted_loci_list()) > 5)
        self.assertTrue('16S rRNA' in self.sra_obj.get_targetted_loci_list())

    def test_get_library_source_list(self):
        # print("test get_library_source_list")
        # print(self.sra_obj.get_library_source_list())
        self.assertTrue(len(self.sra_obj.get_library_source_list()) > 5)
        self.assertTrue('TRANSCRIPTOMIC' in self.sra_obj.get_library_source_list())

    def test_get_instrument_list(self):
        # print("test get_instrument_list")
        # print(self.sra_obj.get_instrument_list())
        self.assertTrue(len(self.sra_obj.get_instrument_list()) > 5)
        self.assertTrue('Illumina HiSeq 1500' in self.sra_obj.get_instrument_list())

    def test_get_platform_list(self):
        # print("test get_platform_list")
        self.assertTrue(len(self.sra_obj.get_platform_list()) > 5)
        self.assertTrue('ILLUMINA' in self.sra_obj.get_platform_list())


if __name__ == '__main__':
    print("do some testing of output methods in extract_experiment_XML_vals.py")
    ic.disable()
    unittest.main()

