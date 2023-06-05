#!/usr/bin/env python3
import unittest
from icecream import ic
ic.disable()
import sys
from attr import define

import ExperimentChecklists2Json
from ExperimentChecklists2Json import *
ic.disable()

base_dir = '/Users/woollard/projects/easi-genomics/ExperimentChecklist/'


class TestExperimentChecklists2Json(unittest.TestCase):
    def setUp(self):
        print("\nRunning setUp method...")
        config_data = self.test_get_config_data()
        expt_objects = ExperimentChecklists2Json.process_and_get_fields(config_data)
        self.assertEqual(len(expt_objects), 14)
        for expt_type in expt_objects:
            print("\t", expt_type)
            ic()
            expt_object = expt_objects[expt_type]
            ic(expt_object)
            self.assertIsInstance(expt_object, ExperimentType)
            ic(expt_object.experiment_type_name)
            self.test_expt_object = expt_object
            break
    def tearDown(self):
        print("Running tearDown method...")

    def test_file2json(self):
        schema_json_file = base_dir + 'data/testing/METABARCODING.json'
        json_obj = file2json(schema_json_file)
        self.assertIsInstance(json_obj,object)

    def test_get_config_data(self):
        ic()
        debug_status = True
        config_data = ExperimentChecklists2Json.read_config(debug_status)
        # ic(config_data)
        self.assertEqual(config_data["adapter_fields"]["adapters"], "")
        return config_data


    def set_expt_type_obj(self, experiment_type_obj):
        ic()
        ic(experiment_type_obj)
        self._experiment_type_obj = experiment_type_obj
        ic(self._experiment_type_obj)
        ic(self._experiment_type_obj.experiment_type_name)
        ic()
        um = self.get_expt_type_obj()
        ic(um.experiment_type_name)
        ic()

    def get_expt_type_obj(self):
        ic()
        ic(self)
        experiment_type_obj = self._experiment_type_obj
        ic(experiment_type_obj)
        ic(experiment_type_obj.experiment_type_name)
        ic()
        return experiment_type_obj

    def test_expt_init(self):
        ic()
        print("inside test_expt_init<----------------------")

        expt_object = self.test_expt_object

        self.assertEqual(expt_object.experiment_type_name, 'METABARCODING')
        self.examine_expt_object(expt_object)
        self.set_expt_type_obj(expt_object)

        ic()

    def test_expt_obj(self):
        ic()
        print("inside test_expt_objs<----------------------")
        expt_type_obj = self.test_expt_object
        self.assertEqual(expt_type_obj.experiment_type_name, 'METABARCODING')

        json_file_name = base_dir + 'data/testing/METABARCODING.json'
        json_obj = file2json(json_file_name)
        print(json_obj)

        ic()
        ic(expt_type_obj.get_special_fields_list())
        test_list = ['pcr_fields', 'target_fields', 'multiplex_fields', 'adapter_fields']
        test_list = ['pcr_fields', 'custom_user_fields']

        self.assertListEqual(expt_type_obj.get_special_fields_list(), test_list)
        test_dict = {'adapters': '',  'multiplex_identifiers': '',
                                       'pcr_primers': {'fwd_name': '', 'fwd_seq': '', 'rev_name': '', 'rev_seq': ''},
                                       'pcr_protocol': '',
                                       'target_loci': '',
                                       'target_subfragment': ''}
        test_dict =        {'pcr_protocol': '',
                            'pcr_primers': {'fwd_name': '', 'fwd_seq': '', 'rev_name': '', 'rev_seq': ''
                                            },
                            'experiment_attribute': {'experiment_context_type': 'baseline', 'key_experimental_factors': [],
                                  '_insert_field_a': '', '_insert_field_b': '', '_insert_field_c': ''}
                            }

        print("££££££££££$$ SPECIAL £££££££££££££")
        print(expt_type_obj.get_special_dict())
        print("££££££££££$$ END SPECIAL £££££££££££££")
        self.assertTrue( test_dict, test_dict | expt_type_obj.get_special_dict(),)
        json_file_name = base_dir + 'data/testing/METABARCODING.json'
        test_dict = file2json(json_file_name)
        self.assertEqual(expt_type_obj.get_all_dict(),expt_type_obj.get_all_dict() | test_dict )

        ic()
        #sys.exit()

    def test_schema_objs(self):
        print("inside test_schema_objs<----------------------")
        config_data = self.test_get_config_data()
        expt_objects = ExperimentChecklists2Json.process_and_get_fields(config_data)
        schema_obj_dict = ExperimentChecklists2Json.create_schema_objects(expt_objects, config_data)
        for expt_type_name in schema_obj_dict:
            ic(expt_type_name)
            schema_obj = schema_obj_dict[expt_type_name]
            ic(schema_obj.experiment_type_name)

            self.assertEqual(schema_obj.experiment_type_name, 'METABARCODING')

            json_file_name = base_dir + 'data/testing/METABARCODING_schema.json'
            test_schema_dict = file2json(json_file_name)

            #self.assertDictContainsSubset(schema_obj.get_experiment_specific_dict(), experiment_specific_dict)

            print("££££££ from program £££££")
            print(schema_obj.get_json_schema())
            print("££££££ from test £££££")
            print(test_schema_dict)
            self.maxDiff = None

            test_json_schema = test_schema_dict
            # self.assertEqual( schema_obj.get_json_schema(), schema_obj.get_json_schema() | test_json_schema)
            break  # only want loop called once




    def examine_expt_object(self, expt_object):
        ic()
        self._expt_object = expt_object
        ic(self._expt_object)




if __name__ == '__main__':
    ic("do some testing")
    ic.disable()
    #sys.exit()
    unittest.main()
