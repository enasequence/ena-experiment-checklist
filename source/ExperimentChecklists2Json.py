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


class ExperimentType:
    """ ExperimentType object
    params:
        in: experiment_type string
    """

    def __init__(self, experiment_type):
        self._special_dict = None
        self._special_fields_list = None
        self._core_dict = None
        self._checklist_dict = None
        self.experiment_type = experiment_type

    def set_special_fields_list(self, special_fields_list):
        self._special_fields_list = special_fields_list
    
    def get_special_fields_list(self):
        return self._special_fields_list

    def set_checklist_dict(self, checklist_dict):
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
        ic(special_dict)
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
        :type experimenttype: object
        ,config_data
    """
    local_dict = {}
    special_keys = list(experimenttype.get_special_fields_list())
    for jsonKey in special_keys:
        if jsonKey in config_data:
            local_dict = {**local_dict, **config_data[jsonKey]}
        else:
            ic('WARN "special" key does not exist: "' + jsonKey + '" please check the config data in the input JSON file'
               +' for *_fields')
    experimenttype.set_special_dict(local_dict)

    return


def get_fields(config_data):
    """ method to get all the fields needed for a particular checklist and to instruct the printing
        of the combined fields JSON to a file 
        in: config_data
        rtn: mergedChecklistDict
    """
    coreDict = get_core_dict(config_data)
    expt_objects = {}
    for etype in config_data['experimentTypes']:
        # ic(etype)
        #create a dictionary of ExperimentType objects index on the name of the experimentType
        experimentType = ExperimentType(etype["experiment_type"])
        expt_objects[experimentType.experiment_type] = experimentType

        # during debugging, concentrate one at a time.
        if experimentType.experiment_type == "TEST":
            ic("good! experiment_type=",experimentType.experiment_type)
        else:
            ic("not expt type, so skipping", experimentType.experiment_type)
            continue
        experimentType.set_checklist_dict(etype)
        experimentType.set_core_dict(coreDict)
        add_specials(experimentType, config_data)

        experimentType.print_checklist()


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


def main():
    config_data = read_config()
    get_fields(config_data)


if __name__ == '__main__':
    main()
