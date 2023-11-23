#!/usr/bin/env python3
""" ExperimentChecklists2Json.py
Script to computationally generate the experimental checklist JSON files for users to enter data into.

* It is driven by a single JSON config file in data/input.
* class ExperimentType - for handling generating the Json user checklist for each ExperimentType
* class ExperimentTypeJsonSchema - for handling generating the Json schema to validate each ExperimentType
* The JSON experiment type checklists are created 1 per experiment type in the data/output
* The JSON schema files are created 1 per checklist in the data/schema directory

The single JSON config file will need to be maintained for a number of aspects including:
* new experiment types
* changes to the specific

This script, configuration JSON and outputs ought to be considered prototypes,
to explore what can be done and what is needed.

Weaknesses currently:

* the JSON config needs to be manually edited
* very little testing is being done (need to add many more tests!)

___author___ = "woollard@ebi.ac.uk"
___start_date___ = "2022-11-29"
__docformat___ = 'reStructuredText'

"""
import pandas as pd
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
# python3 -m pydoc -w ExperimentChecklists2Json

from icecream import ic
# import re
# import os
# from os.path import join, dirname
# import json
# import sys
# ic.disable()
from extract_experiment_XML_vals import *
from ChecklistDoc import ChecklistDoc
# from ExperimentTypeJsonSchema.ExperimentTypeJsonSchemaClass import ExperimentTypeJsonSchemaClass
from ExperimentTypeJsonSchema import *
from ExperimentType import ExperimentType
from ExperimentUtils import get_data_locations, writeString2file

# from ExperimentChecklist import *
# from jsonschema import validate
# import pandas as pd

global glob_exp_obj
base_dir = '/Users/woollard/projects/easi-genomics/ExperimentChecklist/'

""" ########################"Normal routine"#####################################
"""


def get_core_dict(config_data):
    """
    extract the core fields as JSON entries
    params:
        in: the full config_json
        rtn: coreDict elements of the config_json
        and coreDictDefaults, as above, but has the default_values
    """

    coreDict = {}
    coreDictDefaultVal = {}
    for field in config_data['coreFields']:
        if "_comment" in field:
            continue
        # if field not in ["library_source"]:
        #    continue
        if isinstance(config_data['coreFields'][field], dict):
            # ic(field, " in config_data", config_data['coreFields'][field])
            if config_data['coreFields'][field]['type'] == 'number':
                # ic(config_data['coreFields'][field])
                coreDict[field] = config_data['coreFields'][field]['default']
                """as they are numeric, the JSON wants a number not a string"""
            else:
                coreDict[field] = ""

            if (coreDict[field] != "") and ("default" in config_data['coreFields'][field]):
                coreDictDefaultVal[field] = coreDict[field]
                # ic("first if:", coreDictDefaultVal[field])
            elif "default" in config_data['coreFields'][field]:
                # ic(config_data['coreFields'][field]['default'])
                coreDictDefaultVal[field] = config_data['coreFields'][field]['default']
                #ic("el if:", coreDictDefaultVal[field])
            else:
                coreDictDefaultVal[field] = ""
                # ic("else :", coreDictDefaultVal[field])
            # ic(type(config_data['coreFields'][i]))
            # ic("dict: " + str(config_data['coreFields'][i]))
        else:
            # ic(field, " not in config_data['coreFields']")
            # ic("!dict:" + str(config_data['coreFields'][i]))
            coreDictDefaultVal[field] = coreDict[field] = config_data['coreFields'][field]
    return coreDict, coreDictDefaultVal


def add_specials(experiment_type: object, config_data: object) -> object:
    """ method to check for and pull out the json for special field cases in 
        each checklist, from the config_data file.
        The special fields like pcr_fields pull in a more complex JSON dict from the config_data
        sets the special fields JSON for each experiment type
    params:
        in:
        :type experiment_type: object,
        :param config_data:

    """
    local_dict = {}
    special_keys = list(experiment_type.get_special_fields_list())
    # print(experiment_type.experiment_type_name)
    # ic.enable()
    for jsonKey in special_keys:
        #ic(jsonKey)
        if jsonKey in config_data:
            #ic(config_data[jsonKey])
            local_dict = {**local_dict, **config_data[jsonKey]}
            #ic(local_dict)
        else:
            print('WARN "special" key does not exist: "' + jsonKey +
               '" please check the config data in the input JSON file' + ' for *_fields')
    experiment_type.set_special_dict(local_dict)
    return


def process_and_get_fields(config_data):
    """ method to get all the fields and values needed for a particular checklist as JSON
        in: config_data
        rtn: Dict of experimentType objects
    """
    (coreDict, coreDictDefaultVal) = get_core_dict(config_data)
    expt_objects_dict = {}
    for e_type_slice in config_data['experimentTypes']:

        # create a dictionary of ExperimentType objects index on the name of the experimentType
        experimentType = ExperimentType(e_type_slice["experiment_type"])
        # if experimentType not in ["TEST"]:
        #     continue
        expt_objects_dict[experimentType.experiment_type_name] = experimentType

        # during debugging, concentrate one at a time.
        # if experimentType.experiment_type == "TEST":
        #     ic("good! experiment_type=",experimentType.experiment_type)
        # else:
        #     ic("not expt type, so skipping", experimentType.experiment_type)
        #     continue
        experimentType.set_checklist_specific_dict(e_type_slice)
        experimentType.set_core_dict(coreDict)
        experimentType.set_core_dict_default(coreDictDefaultVal)
        add_specials(experimentType, config_data)
    return expt_objects_dict



def print_all_checklists(expt_objects):
    """ print_all_checklists
        params:
        in: expt_objects dict
        rtn: nowt
    """

    combined_cl_df = pd.DataFrame()
    data_loc_dict = get_data_locations()
    output_dir = data_loc_dict["output_xlsx_dir"]
    keys = list(expt_objects.keys())
    first_expt = expt_objects[keys[0]]
    out_file = output_dir + "all_experiment_core.xlsx"
    df = first_expt.get_checklist_as_df()
    ic(out_file)
    df.to_excel(out_file)

    for experiment_type_name in expt_objects:
        experimentType = expt_objects[experiment_type_name]
        experimentType.print_checklist()
        # experimentType.print_test_checklist()
        expt_cl_df = experimentType.get_checklist_as_df()
        ic()
        sys.exit()


def create_schema_objects(expt_objects, config_data):
    """ create_schema_objects
        params:
        in: expt_objects, config_data
        rtn: schema_objects_dict
    """
    #ic()
    schema_objects = {}
    for experiment_type_name in expt_objects:
        experimentType: object = expt_objects[experiment_type_name]
        schema_objects[experiment_type_name] = ExperimentTypeJsonSchemaClass(experimentType, config_data)
        schema_obj = schema_objects[experiment_type_name]
        experimentType.set_json_schema_obj(schema_obj)
        schema_obj.print_json_schema()
    return schema_objects

def print_all_checklist_json_schemas(expt_objects):

    for experiment_type_name in expt_objects:
        experimentType = expt_objects[experiment_type_name]
        schema_obj = experimentType.get_json_schema_obj()
        # ic(schema_obj)
        # print(schema_obj.experiment_type_name)
        # print(schema_obj.get_core_fields_dict())
        # print(schema_obj.get_core_rules_list())
        # print(schema_obj.print_json_schema())
        experimentType.print_ExperimentTypeObj()

def get_an_experiment_type_obj():
    ic()
    config_data = read_config(False)
    expt_objects_dict = process_and_get_fields(config_data)
    schema_obj_dict = create_schema_objects(expt_objects_dict, config_data)
    schema_obj = schema_obj_dict[experiment_type_name]

    experiment_type_name = 'METABARCODING'
    ic()
    ic(expt_objects_dict.keys())
    experimentType = expt_objects_dict[experiment_type_name]
    experimentType.set_json_schema_obj(schema_obj)
    return experimentType


def main():
    ic()
    debug_status = True
    debug_status = False
    checklist_doc = ChecklistDoc()
    config_data = read_config(debug_status)
    expt_objects_dict = process_and_get_fields(config_data)
    schema_obj_dict = create_schema_objects(expt_objects_dict, config_data)

    #experimentType = get_an_experiment_type_obj()
    #ic(experimentType.getCoreExperimentTypeDf())
    # print("## Create expt_objects_dict for each experiment: (they get used later")
    for experiment_type_name in expt_objects_dict:
        # if experiment_type_name != 'TEST_type':
        #     continue
        #print(experiment_type_name)
        ic(experiment_type_name)
        experimentType = expt_objects_dict[experiment_type_name]
        schema_obj = experimentType.get_json_schema_obj()
        ic(schema_obj.get_experiment_type_name())
        #checklist_doc.addExperimentInfo(experimentType)
        ic(experimentType.getSpecificExperimentTypeDf())

        sys.exit()
        #ic(experimentType.get_ExperimentTypeObj_values())
    #print_all_checklists(expt_objects_dict)
    ic()
    #ic(checklist_doc.getCoreExperimentTypeDf())
    ic(checklist_doc.getSpecificExperimentTypeDf())
    #
    #print_all_checklist_json_schemas(expt_objects_dict)

    print("-" * 100)
    print(f"debug_status = {debug_status}")
    for experiment_type_name in schema_obj_dict:
        if debug_status is False and experiment_type_name == "TEST_type":
            continue
        else:
            pass
        print(f"| {experiment_type_name} | ", end="")
        schema_obj = schema_obj_dict[experiment_type_name]
        # ic(schema_obj.experiment_type_name)
        # print(f".print_json_schema {schema_obj.print_json_schema()}")
        experimentType = schema_obj.get_experiment_type_obj()
        experimentType.print_checklist()
        print(f"checklist created | ", end="")
        experimentType.set_json_schema_obj(schema_obj)
        checklist_doc.addExperimentInfo(experimentType)
        print(f"schema created | ", end = "")
        print("")
        print("-" * 100)

    checklist_doc.print_checklist_doc()
    ic("at the end of main in the initialising script")


if __name__ == '__main__':
    main()
