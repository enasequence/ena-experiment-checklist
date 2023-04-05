#!/usr/bin/env python3
import unittest
from icecream import ic
#ic.disable()
import sys
from attr import define

import ExperimentChecklists2Json

class TestExperimentChecklists2Json(unittest.TestCase):

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
        config_data = self.test_get_config_data()
        expt_objects = ExperimentChecklists2Json.process_and_get_fields(config_data)
        self.assertEqual(len(expt_objects), 1)
        for expt_type in expt_objects:
            ic()
            expt_object = expt_objects[expt_type]
            ic(expt_object)
            #self.assertIsInstance(expt_object, type(ExperimentType))
            ic(expt_object.experiment_type_name)
            self.assertEqual(expt_object.experiment_type_name, 'TEST_type')
            self.examine_expt_object(expt_object)
            self.set_expt_type_obj(expt_object)
            global global_exp_type_obj
            global_exp_type_obj = expt_object
            break
        ic()

    def test_expt_obj(self):
        ic()
        expt_type_obj = global_exp_type_obj
        self.assertEqual(expt_type_obj.experiment_type_name, 'TEST_type')
        ic()
        ic(expt_type_obj.get_special_fields_list())
        test_list = ['pcr_fields', 'target_fields', 'multiplex_fields', 'adapter_fields']
        self.assertListEqual(expt_type_obj.get_special_fields_list(), test_list)
        test_dict = {'adapters': '',  'multiplex_identifiers': '',
                                       'pcr_primers': {'fwd_name': '', 'fwd_seq': '', 'rev_name': '', 'rev_seq': ''},
                                       'pcr_protocol': '',
                                       'target_loci': '',
                                       'target_subfragment': ''}
        self.assertDictContainsSubset(expt_type_obj.get_special_dict(), test_dict)
        test_dict = {'adapters': '',
                                   'checklist_group': 'TEST_group',
                                   'checklist_id': 'EXC00000Z',
                                   'checklist_name': 'TEST_name',
                                   'checklist_version': '20221129',
                                   'experiment_type': 'TEST_type',
                                   'library_source': 'TRANSCRIPTOMIC',
                                   'multiplex_identifiers': '',
                                   'pcr_primers': {'fwd_name': '', 'fwd_seq': '', 'rev_name': '', 'rev_seq': ''},
                                   'pcr_protocol': '',
                                   'target_loci': '',
                                   'target_subfragment': ''}
        self.assertDictContainsSubset(expt_type_obj.get_all_dict(), test_dict)

        ic()
        #sys.exit()

    def test_schema_objs(self):
        config_data = self.test_get_config_data()
        expt_objects = ExperimentChecklists2Json.process_and_get_fields(config_data)
        schema_obj_dict = ExperimentChecklists2Json.create_schema_objects(expt_objects, config_data)
        for expt_type_name in schema_obj_dict:
            ic(expt_type_name)
            schema_obj = schema_obj_dict[expt_type_name]
            ic(schema_obj.experiment_type_name)
            self.assertEqual(schema_obj.experiment_type_name, "TEST_type")

            experiment_specific_dict = {'checklist_group': {'_example': 'TEST_group',
                             'default': 'TEST_group',
                             'description': '',
                             'type': 'string'},
         'checklist_id': {'_example': 'EXC00000Z',
                          'default': 'EXC00000Z',
                          'description': '',
                          'type': 'string'},
         'checklist_name': {'_example': 'TEST_name',
                            'default': 'TEST_name',
                            'description': '',
                            'type': 'string'},
         'checklist_version': {'_example': '20221129',
                               'default': '20221129',
                               'description': '',
                               'type': 'string'},
         'experiment_type': {'_example': 'TEST_type',
                             'default': 'TEST_type',
                             'description': '',
                             'type': 'string'},
         'library_source': {'_example': 'TRANSCRIPTOMIC',
                            'default': 'TRANSCRIPTOMIC',
                            'description': '',
                            'type': 'string'}}

            self.assertDictContainsSubset(schema_obj.get_experiment_specific_dict(), experiment_specific_dict)




    def examine_expt_object(self, expt_object):
        ic()
        self._expt_object = expt_object
        ic(self._expt_object)




if __name__ == '__main__':
    unittest.main()
