# a single comment
"""Script to computationally generate the experimental checklist JSON files for users to enter data into.
It is driven by a single JSON config file.

___author___ = "woollard@ebi.ac.uk"
___start_date___ = "2022-11-29"
__docformat___ = 'reStructuredText'

"""
# python3 -m pydoc -w ExperimentChecklists2Json

from icecream import ic
# import subprocess
# import sys
# import getopt
# import requests
# from requests.structures import CaseInsensitiveDict
import re
# import os
# from os.path import join, dirname
import json


# from jsonschema import validate
# import pandas as pd

class ExperimentTypeJsonSchema:
    def __init__(self, experiment_type_obj: object, core_dict):
        self._experimentType = experiment_type_obj
        self.experiment_type_name = experiment_type_obj.experiment_type_name
        self._core_dict = core_dict

    def get_core_dict(self):
        return self._core_dict

    def get_core_fields_dict(self):
        """get_core_fields_dict
        This already has the
        """
        return self._core_dict['coreFields']

    def get_core_rules_list(self):
        """get_core_fields_dict
        This already has the
        """
        return self._core_dict['coreRules']


class ExperimentType:
    """ ExperimentType object
    params:
        in: experiment_type string
    """

    def __init__(self, experiment_type_name):
        self._json_schema_obj = None
        self._special_dict = None
        self._special_fields_list = None
        self._core_dict = None
        self._checklist_dict = None
        self.experiment_type_name = experiment_type_name

    def set_special_fields_list(self, special_fields_list):
        self._special_fields_list = special_fields_list
    
    def get_special_fields_list(self):
        return self._special_fields_list

    def set_json_schema_obj(self, schema_obj):
        self._json_schema_obj = schema_obj

    def get_json_schema_obj(self):
        return self._json_schema_obj

    def set_checklist_dict(self, checklist_dict):
        """ set_checklist_dict
        this has extra complexity, as it is parsing our and setting the special fields too.
        e.g. prc_fields.
        """
        special_fields = []
        tmp_dict = dict(checklist_dict)
        for key in tmp_dict:
            if re.search("_fields$", key):
                special_fields.append(key)
                del checklist_dict[key]
        self.set_special_fields_list(special_fields)
        self._checklist_dict = checklist_dict

    def get_checklist_dict(self):
        return self._checklist_dict

    def set_special_dict(self, special_dict):
        self._special_dict = special_dict

    def get_special_dict(self):
        return self._special_dict

    def get_core_dict(self):
        return self._core_dict

    def set_core_dict(self, core_dict):
        self._core_dict = core_dict

    def get_all_dict(self):
        all_dict = {**self.get_checklist_dict(), **self.get_core_dict(), **self.get_special_dict()}
        return all_dict

    def print_checklist(self):
        """
        params:

        """
        data_loc_dict = get_data_locations()

        all_checklist_dict = self.get_all_dict()
        # ic(checklistDict)
        outfileName = data_loc_dict["output_dir"] + all_checklist_dict['experiment_type'] + '.json'
        ic(outfileName)

        my_list = [all_checklist_dict]
        json_object = json.dumps(my_list, indent = 4, sort_keys = True)
        with open(outfileName, "w") as outfile:
            outfile.write(json_object)
        return


def get_core_dict(config_data):
    """
    extract the core fields as JSON entries
    params:
        in: the full config_json
        rtn: coreDict elements of the config_json
    """
    # ic(config_data['coreFields'])
    coreDict = {}
    for i in config_data['coreFields']:
        # print(i)
        if isinstance(config_data['coreFields'][i], dict):
            coreDict[i] = ""
            # ic(type(config_data['coreFields'][i]))
            # ic("dict: " + str(config_data['coreFields'][i]))
        else:
            # ic("!dict:" + str(config_data['coreFields'][i]))
            coreDict[i] = config_data['coreFields'][i]
    # ic(coreDict)
    # quit()
    return coreDict


def add_specials(experimenttype: object, config_data: object) -> object:
    """ method to check for and pull out the json for special field cases in 
        each checklist, from the config_data file.
        The special fields like pcr_fields pull in a more complex JSON dict from the config_data
        sets the special fields JSON for each experimemttype
    params:
        in:
        :type experimenttype: object,
        :param config_data:

    """
    local_dict = {}
    special_keys = list(experimenttype.get_special_fields_list())
    for jsonKey in special_keys:
        if jsonKey in config_data:
            local_dict = {**local_dict, **config_data[jsonKey]}
        else:
            ic('WARN "special" key does not exist: "' + jsonKey +
               '" please check the config data in the input JSON file' + ' for *_fields')
    experimenttype.set_special_dict(local_dict)

    return


def get_fields(config_data):
    """ method to get all the fields and values needed for a particular checklist as JSON
        in: config_data
        rtn: Dict of experimentTYpe objects
    """
    coreDict = get_core_dict(config_data)
    expt_objects = {}
    for etype in config_data['experimentTypes']:
        # ic(etype)
        # create a dictionary of ExperimentType objects index on the name of the experimentType
        experimentType = ExperimentType(etype["experiment_type"])
        expt_objects[experimentType.experiment_type_name] = experimentType

        # during debugging, concentrate one at a time.
        # if experimentType.experiment_type == "TEST":
        #     ic("good! experiment_type=",experimentType.experiment_type)
        # else:
        #     ic("not expt type, so skipping", experimentType.experiment_type)
        #     continue
        experimentType.set_checklist_dict(etype)
        experimentType.set_core_dict(coreDict)
        add_specials(experimentType, config_data)

    return expt_objects


def get_data_locations():
    """ get_data_locations
    params:
        rtn: data_loc_dict
    """
    data_loc_dict = {"base_dir": "/Users/woollard/projects/easi-genomics/ExperimentChecklist/"}
    data_loc_dict["input_dir"] = data_loc_dict["base_dir"] + "data/input/"
    data_loc_dict["output_dir"] = data_loc_dict["base_dir"] + "data/output/"

    return data_loc_dict


def read_config():
    """ readConfig
    reads the master JSON file
    This file provides all the JSON data fields etc. that are used to build the different experiment templates
    params:
        rtn: JSON
    """

    data_loc_dict = get_data_locations()
    filename = data_loc_dict["input_dir"] + "ExperimentChecklistIn.json"
    ic(filename)
    f = open(filename)
    data = json.load(f)
    f.close()
    return data


def print_all_checklists(expt_objects):
    """ print_all_checklists
        params:
        in: expt_objects dict
        rtn: nowt
    """
    ic()
    for experiment_type_name in expt_objects:
        ic(experiment_type_name)
        experimentType = expt_objects[experiment_type_name]
        experimentType.print_checklist()


def create_schema_objects(expt_objects, config_data):
    """ print_all_checklists
        params:
        in: expt_objects, config_data
        rtn: schema_objects
    """
    ic()
    schema_objects = {}

    for experiment_type_name in expt_objects:
        ic(experiment_type_name)
        experimentType: object = expt_objects[experiment_type_name]
        schema_obj = ExperimentTypeJsonSchema(experimentType, config_data)
        schema_objects[experiment_type_name] = schema_obj
        experimentType.set_json_schema_obj(schema_obj)

    return schema_objects


def print_all_checklist_json_schemas(expt_objects):
    ic()
    for experiment_type in expt_objects:
        ic(experiment_type)
        experimentType = expt_objects[experiment_type]
        schema_obj = experimentType.get_json_schema_obj()
        ic(schema_obj.experiment_type_name)
        ic(schema_obj.get_core_fields_dict())
        ic(schema_obj.get_core_rules_list())


def main():
    config_data = read_config()
    expt_objects = get_fields(config_data)
    # print_all_checklists(expt_objects)
    create_schema_objects(expt_objects, config_data)
    print_all_checklist_json_schemas(expt_objects)


if __name__ == '__main__':
    main()
