#!/usr/bin/env python3

""" unit test cases for ExperimentTypeJsonSchema.py
 Currently rather limited test cases, partly as some of the data is loaded outwith the object...

___author___ = "woollard@ebi.ac.uk"
___start_date___ = 2023-05-15
__docformat___ = 'reStructuredText'
"""

import unittest
from ExperimentTypeJsonSchema import *
from ExperimentType import ExperimentType

global experiment_type_name
experiment_type_name = "TRANSCRIPTOMICS"


def lists_are_equal(list1, list2):
    return list1 == list2


class Test(unittest.TestCase):

    def setUp(self):
        self.experiment_type = ExperimentType(experiment_type_name)
        config_data = read_config(False)
        self.schema_obj = ExperimentTypeJsonSchemaClass(self.experiment_type, config_data)

    def test_experiment_type_name(self):
        self.assertEqual(self.schema_obj.get_experiment_type_name(), experiment_type_name)

    def test_experiment_type_class(self):
        test_class_type = "<class 'ExperimentType.ExperimentType'>"
        self.assertTrue(type(self.experiment_type), test_class_type)

    def test_experiment_type_json_schema_class(self):
        # ic(type(self.schema_obj))
        test_class_type = "<class 'ExperimentTypeJsonSchema.ExperimentTypeJsonSchemaClass'>"
        self.assertTrue(type(self.schema_obj), test_class_type)

    def test_get_core_dict(self):
        all_core_dict = self.schema_obj.get_core_dict()
        test_keys = ['schemaMetadata', 'experimentTypes', 'pcr_fields', 'custom_user_fields',
                     'non_aligned_sequence_file_fields', 'aligned_sequence_file_fields', 'all_sequence_file_fields',
                     'target_fields', 'multiplex_fields', 'adapter_fields', 'coreFields', 'allSpecificFieldsConfig',
                     'coreRules']
        self.assertTrue(lists_are_equal(test_keys, list(all_core_dict.keys())))

    def test_get_platform_instrument(self):
        test_platform = "ILLUMINA"
        test_instrument = 'Illumina MiSeq'
        platform_instrument_dict = self.schema_obj.get_platform_instrument()
        # ic(type(platform_instrument_dict))
        # ic(platform_instrument_dict.keys())
        self.assertTrue(test_instrument in platform_instrument_dict[test_platform])


if __name__ == '__main__':
    print("do some testing of ExperimentTypeJsonSchema.py")
    ic.disable()
    unittest.main()
