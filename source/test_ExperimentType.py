#!/usr/bin/env python3

""" unit test cases for ExperimentType.py

___author___ = "woollard@ebi.ac.uk"
___start_date___ = 2023-05-15
__docformat___ = 'reStructuredText'
"""

import unittest
from icecream import ic
from ExperimentType import *
from ExperimentUtils import read_config
from ExperimentTypeJsonSchema import *

def create_experiment_type_schema_object(self, experiment_type_name):
    self.experiment_type = ExperimentType(experiment_type_name)
    config_data = read_config(False)
    schema_obj = ExperimentTypeJsonSchemaClass(self.experiment_type, config_data)
    self.experiment_type.set_json_schema_obj(schema_obj)

def lists_are_equal(list1, list2):
    return list1 == list2
class Test(unittest.TestCase):

    def setUp(self):
        experiment_type_name = 'TRANSCRIPTOMICS'
        create_experiment_type_schema_object(self, experiment_type_name)

    def test_experiment_type(self):
        ic()
        self.assertTrue(type(self.experiment_type), "<class 'ExperimentType.ExperimentType'>")

    def test_read_config(self):
        config_data = read_config(False)
        test_config_key_list = ['schemaMetadata', 'experimentTypes', 'pcr_fields', 'custom_user_fields', 'non_aligned_sequence_file_fields',
         'aligned_sequence_file_fields', 'all_sequence_file_fields', 'target_fields', 'multiplex_fields',
         'adapter_fields', 'coreFields', 'allSpecificFieldsConfig', 'coreRules']
        ic(config_data.keys())
        self.assertTrue(lists_are_equal(test_config_key_list, list(config_data.keys())))


    def test_experiment_type_name(self):
        ic()
        ic(self.experiment_type.get_experiment_type_name())
        self.assertTrue(self.experiment_type.get_experiment_type_name() == "TRANSCRIPTOMICS")

    def test_checklist_specific_dict(self):
        ic()
        ic(self.experiment_type.get_checklist_specific_dict())
        self.assertFalse(self.experiment_type.get_checklist_specific_dict(), None)


    # def test_get_platform_instrument(self):
    #     self.experiment_type.get_platform_instrument(self)

if __name__ == '__main__':
    print("do some testing of output methods in ExperimentType.py")
    ic.enable()
    unittest.main()
