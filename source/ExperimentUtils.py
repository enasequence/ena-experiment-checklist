"""
Experiment utils
"""
import json

def get_base_dir():
    return "/Users/woollard/projects/easi-genomics/ExperimentChecklist/"

def get_data_locations():
    """ get_data_locations
    params:
        rtn: data_loc_dict
    """
    data_loc_dict = {}
    data_loc_dict["base_dir"] = get_base_dir()
    data_dir = data_loc_dict["base_dir"] + "data/"
    data_loc_dict["input_dir"] = data_dir + "input/"
    data_loc_dict["output_dir"] = data_dir + "output/"
    data_loc_dict["output_xlsx_dir"] = data_dir + "output_xlsx/"
    data_loc_dict["output_test_dir"] = data_dir + "output_test/"
    data_loc_dict["schema_dir"] = data_dir + "schema/"
    return data_loc_dict

def file2json(filename):
    f = open(filename, "r")
    json_obj = json.load(f)
    f.close()
    #ic(json_obj)
    return json_obj

def writeString2file(out_string, out_filename):
    text_file = open(out_filename, 'w')
    text_file.write(out_string)
    text_file.close()

def read_config(debug_status):
    """ readConfig
    reads the master JSON file
    This file provides all the JSON data fields etc. that are used to build the different experiment templates
    params:
        rtn: JSON
    """

    data_loc_dict = get_data_locations()
    if not debug_status:
        filename = data_loc_dict["input_dir"] + "ExperimentChecklistIn.json"
    else:
        filename = data_loc_dict["input_dir"] + "test_ExperimentChecklistIn.json"
    print(filename)
    f = open(filename)
    data = json.load(f)
    f.close()
    return data
