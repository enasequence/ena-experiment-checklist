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

from ChecklistDoc import ChecklistDoc
from ExperimentType import process_and_get_fields2expt_type_obj_dict
# from ExperimentTypeJsonSchema.ExperimentTypeJsonSchemaClass import ExperimentTypeJsonSchemaClass
from ExperimentTypeJsonSchema import *
from ExperimentUtils import get_data_locations
from extract_experiment_XML_vals import *

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
# python3 -m pydoc -w ExperimentChecklists2Json

# from ExperimentChecklist import *
# from jsonschema import validate
# import pandas as pd

global glob_exp_obj
base_dir = '/Users/woollard/projects/easi-genomics/ExperimentChecklist/'

""" ########################"Normal routine"#####################################
"""


def print_all_checklists(expt_objects):
    """ print_all_checklists
        params:
        in: expt_objects dict
        rtn: nowt
    """
    ic()
    pd.DataFrame()
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

def create_schema_objects(expt_objects, config_data):
    """ create_schema_objects
        params:
        in: expt_objects, config_data
        rtn: schema_objects_dict
    """
    # ic()
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
        # schema_obj = experimentType.get_json_schema_obj()
        # ic(schema_obj)
        # print(schema_obj.experiment_type_name)
        # print(schema_obj.get_core_fields_dict())
        # print(schema_obj.get_core_rules_list())
        # print(schema_obj.print_json_schema())
        experimentType.print_ExperimentTypeObj()


def get_an_experiment_type_obj():
    ic()
    experiment_type_name = 'METABARCODING'

    config_data = read_config(False)
    expt_objects_dict = process_and_get_fields2expt_type_obj_dict(config_data)
    schema_obj_dict = create_schema_objects(expt_objects_dict, config_data)
    schema_obj = schema_obj_dict[experiment_type_name]
    ic(expt_objects_dict.keys())
    experimentType = expt_objects_dict[experiment_type_name]
    experimentType.set_json_schema_obj(schema_obj)
    return experimentType


def generate_checklist_files(expt_objects_dict, schema_obj_dict, checklist_doc, debug_status):
    """

    :param checklist_doc:
    :param expt_objects_dict:
    :param schema_obj_dict:
    :param debug_status:
    :return:
    """
    # print("## Create expt_objects_dict for each experiment: (they get used later")
    expt_keys = list(expt_objects_dict)
    ic(expt_keys)
    for experiment_type_name in expt_keys:
        # if experiment_type_name != 'TEST_type':
        #     continue
        # print(experiment_type_name)
        ic(experiment_type_name)
        # experimentType = expt_objects_dict[experiment_type_name]
        # ic(experimentType.get_checklist_specific_dict())
        # ic(experimentType.getSpecificExperimentTypeDf())

    ic()
    print("-" * 100)
    print(f"debug_status = {debug_status}")
    for experiment_type_name in schema_obj_dict:
        if debug_status is False and experiment_type_name == "TEST_type":
            continue
        else:
            pass
        print(f"| {experiment_type_name} | ", end = "")
        schema_obj = schema_obj_dict[experiment_type_name]
        # ic(schema_obj.experiment_type_name)
        # print(f".print_json_schema {schema_obj.print_json_schema()}")
        experimentType = schema_obj.get_experiment_type_obj()
        experimentType.print_checklist()
        print(f"checklist created | ", end = "")
        experimentType.set_json_schema_obj(schema_obj)
        checklist_doc.addExperimentInfo(experimentType)
        print(f"schema created | ", end = "")
        print("")
        print("-" * 100)


def main():
    ic()
    data_loc_dict = get_data_locations()
    ic(data_loc_dict)
    debug_status = False
    checklist_doc = ChecklistDoc()
    config_data = read_config(debug_status)
    expt_objects_dict = process_and_get_fields2expt_type_obj_dict(config_data)
    # print("-----------------------------------------------------------------------------")
    # ic()
    # metabarcoding_eT = expt_objects_dict['METABARCODING']
    # ic(metabarcoding_eT.get_checklist_specific_dict())
    # print("-----------------------------------------------------------------------------")
    schema_obj_dict = create_schema_objects(expt_objects_dict, config_data)

    # getting any experiment_type_onk
    experimentType = get_an_experiment_type_obj()
    out_file_name = data_loc_dict['output_xlsx_dir'] + "all_core_experiment_metadata.xlsx"
    ic(out_file_name)
    experimentType.getCoreExperimentTypeDf().to_excel(out_file_name, index = False)
    # need to fix the controlled vocab terms!

    print("-----------------------------------------------------------------------------")

    generate_checklist_files(expt_objects_dict, schema_obj_dict, checklist_doc, debug_status)

    checklist_doc.print_checklist_doc()
    ic("at the end of main in the initialising script")


if __name__ == '__main__':
    main()
