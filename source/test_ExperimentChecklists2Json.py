import unittest
from icecream import ic

import ExperimentChecklists2Json


class TestExperimentChecklists2Json(unittest.TestCase):

    def get_etype(self):
        etype = {}
        etype["experiment_type"] = '''{
          "checklist_id": "EXC00000Z",
          "checklist_name": "TEST specific",
          "checklist_group": "TEST",
          "checklist_version": "20221129",
          "experiment_type": "TEST",
          "library_source": "ALL SPECIFIC FIELDS",
          "pcr_fields": "",
          "target_fields": "",
          "multiplex_fields": "",
          "adapter_fields": ""
        }'''
        return etype

    def set_obj(self, experiment_type_obj):
        ic()
        ic(experiment_type_obj)
        self._experiment_type_obj = experiment_type_obj

    def get_obj(self):
        ic()
        ic(self._experiment_type_obj)
        return self._experiment_type_obj

    def test_experiment_type_init(self):
        etype = self.get_etype()
        experiment_type = ExperimentChecklists2Json.ExperimentType(etype["experiment_type"])
        self.set_obj(experiment_type)
        ic()
        self.assertIsInstance(experiment_type, ExperimentChecklists2Json.ExperimentType)  # add assertion here

    def test_experiment_type_name(self):
        experiment_type = self.get_obj()
        self.assertEqual(experiment_type.experiment_type_name, "FF")


if __name__ == '__main__':
    unittest.main()
