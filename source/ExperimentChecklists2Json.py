# a single comment
"""Script to computationally generate the experimental checklist JSON files for users to enter data into.

* It is driven by a single JSON config file.
* class ExperimentType -  for handling generating the Json user checklist for each ExperimentType
* class ExperimentTypeJsonSchema - for handling generating the Json schema to validate each ExperimentType

___author___ = "woollard@ebi.ac.uk"
___start_date___ = "2022-11-29"
__docformat___ = 'reStructuredText'

"""
# python3 -m pydoc -w ExperimentChecklists2Json

from icecream import ic
import re
# import os
# from os.path import join, dirname
import json

from mergedeep import merge


# from jsonschema import validate
# import pandas as pd

class ExperimentTypeJsonSchema:
    """ ExperimentTypeJsonSchema
    for handling generating the Json schema to validate each specific ExperimentType
        N.B. Currently many of the sets are not being done as they are slices of the core_dict
    """

    def __init__(self, experiment_type_obj: object, core_dict):
        ic()
        self._experimentType = experiment_type_obj
        self.experiment_type_name = experiment_type_obj.experiment_type_name
        self._core_dict = core_dict
        self.set_experiment_specific_dict(experiment_type_obj.get_checklist_specific_dict())

    def get_core_dict(self):
        return self._core_dict

    def get_core_fields_dict(self):
        """get_core_fields_dict
        This already has the JSON schema attributes
        """
        return self._core_dict['coreFields']

    def get_core_rules_list(self):
        """get_core_fields_dict

        """
        return self._core_dict['coreRules']

    def get_schema_metadata(self):
        """get_schema_metadata
        """
        return self._core_dict['schemaMetadata']

    def get_all_specific_fields_json_config(self):
        """get_all_specific_fields_json_config
                """
        return self._core_dict["allSpecificFieldsConfig"]

    def set_experiment_specific_dict(self, experiment_specific_dict):
        """set_experiment_specific_dict
           These are getting the JSON configuration for the non-core fields
           only a subsection of the non-core fields are needed for each experiment type
           + making use of the default and examples from the specific experiment fields.
        """
        ic(experiment_specific_dict)
        all_specific_dict = self.get_all_specific_fields_json_config()
        my_specific_json_config = {}
        for field in experiment_specific_dict:
            if field in all_specific_dict:
                my_specific_json_config[field] = all_specific_dict[field]
                my_specific_json_config[field]["default"] = experiment_specific_dict[field]
                my_specific_json_config[field]["_example"] = my_specific_json_config[field]["default"]
            else:
                ic("WARNING: need to add json config for ", field)
        ic(my_specific_json_config)
        self._specific_json_config = my_specific_json_config

    def get_experiment_specific_dict(self):
        """get_experiment_specific_dict
          getting the experiment type specific JSON configuration ( i.e. not the core fields )
          effectively many of the fields are core, but the assigned values are not, hence handling this way.
        """
        return self._specific_json_config

    def get_json_schema(self):
        """ get_json_schema
        generate a JSON_schema as a python schema specific to an experiment type
        This will ultimately be printed out as a json schema to validate the experiment_type
        return schema_dict
        """
        ic("=" * 80)
        schema_core_dict = {"checklists": {"checklist_fields_core": {"properties": self.get_core_fields_dict()}}}
        schema_rules_dict = {"checklists": {"checklist_fields_core": {"allOf": self.get_core_rules_list()}}}
        experiment_type_specific_dict = {"checklists": {"checklist_fields_core":
                                                        {"allOf": self.get_experiment_specific_dict()}}}
        # cl_metadata_dict["checklists"] = self.get_schema_metadata()
        """N.B. this does a deep merge of the dictionaries, most other methods did not..."""
        schema_dict = merge(schema_rules_dict, schema_core_dict, self.get_schema_metadata(),
                            experiment_type_specific_dict)
        # **json_schema_dict}
        ic(schema_dict)

        return schema_dict

    def print_json_schema(self):
        """ print_json_schema
        params:

        """
        data_loc_dict = get_data_locations()

        json_schema_dict = self.get_json_schema()
        # ic(checklistDict)
        outfileName = data_loc_dict["schema_dir"] + self.experiment_type_name + '_schema.json'
        ic(outfileName)

        """Create a list as top level """
        my_list = [json_schema_dict]
        json_object = json.dumps(my_list, indent = 4, sort_keys = True)
        with open(outfileName, "w") as outfile:
            outfile.write(json_object)

        return


class ExperimentType:
    """ ExperimentType object
    for handling generating the Json user checklist for each ExperimentType
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

    def set_checklist_specific_dict(self, checklist_dict):
        """ set_checklist_specific_dict
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

    def get_checklist_specific_dict(self):
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
        all_dict = {**self.get_checklist_specific_dict(), **self.get_core_dict(), **self.get_special_dict()}
        return all_dict

    # def print_checklist(self):
    #     """
    #     params:
    #     deprecated
    #     """
    #     data_loc_dict = get_data_locations()
    #
    #     all_checklist_dict = self.get_all_dict()
    #     # ic(checklistDict)
    #     outfileName = data_loc_dict["output_dir"] + all_checklist_dict['experiment_type'] + '.json'
    #     ic(outfileName)
    #
    #     my_list = [all_checklist_dict]
    #     json_object = json.dumps(my_list, indent = 4, sort_keys = True)
    #     with open(outfileName, "w") as outfile:
    #         outfile.write(json_object)
    #     return


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
    for jsonKey in special_keys:
        if jsonKey in config_data:
            local_dict = {**local_dict, **config_data[jsonKey]}
        else:
            ic('WARN "special" key does not exist: "' + jsonKey +
               '" please check the config data in the input JSON file' + ' for *_fields')
    experiment_type.set_special_dict(local_dict)

    return


def get_fields(config_data):
    """ method to get all the fields and values needed for a particular checklist as JSON
        in: config_data
        rtn: Dict of experimentTYpe objects
    """
    coreDict = get_core_dict(config_data)
    expt_objects = {}
    for e_type in config_data['experimentTypes']:
        # ic(e_type)
        # create a dictionary of ExperimentType objects index on the name of the experimentType
        experimentType = ExperimentType(e_type["experiment_type"])
        expt_objects[experimentType.experiment_type_name] = experimentType

        # during debugging, concentrate one at a time.
        # if experimentType.experiment_type == "TEST":
        #     ic("good! experiment_type=",experimentType.experiment_type)
        # else:
        #     ic("not expt type, so skipping", experimentType.experiment_type)
        #     continue
        experimentType.set_checklist_specific_dict(e_type)
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
    data_loc_dict["schema_dir"] = data_loc_dict["base_dir"] + "data/schema/"

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
        ic(schema_obj.print_json_schema())


def main():
    ic()
    config_data = read_config()
    expt_objects = get_fields(config_data)
    # print_all_checklists(expt_objects)
    create_schema_objects(expt_objects, config_data)
    print_all_checklist_json_schemas(expt_objects)


if __name__ == '__main__':
    main()
