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
import re
# import os
# from os.path import join, dirname
import json
import sys

from mergedeep import merge
ic.disable()
from extract_experiment_XML_vals import *

# from ExperimentChecklist import *
ic.disable()

# from jsonschema import validate
# import pandas as pd

global glob_exp_obj
base_dir = '/Users/woollard/projects/easi-genomics/ExperimentChecklist/'

def file2json(filename):
    ic(filename)
    f = open(filename, "r")
    json_obj = json.load(f)
    f.close()
    ic(json_obj)
    return json_obj

def writeString2file(out_string, out_filename):
    print(out_filename)
    text_file = open(out_filename, 'w')
    text_file.write(out_string)
    text_file.close()

class ChecklistDoc:
    """
    Create md documentation for the experiments type checklists

    """
    def __init__(self):
        self.title = '# experiments type checklists\n'
        self.intro = '## Introduction\n\n' + 'These are the checklists for different types of experiments.\n'
        self.intro + "This documentation is automatically built from the templates\n\n"
        self.overall = """## Overall: how and what needs to be submitted

For experiment metadata one needs a minimal mandatory amount of metadata fields and values.

* sample_id
* study_id
* instrument_model
* library_name
* library_source
* library_strategy

and one or more:

* sequence file name and associated checksum

see <https://ena-docs.readthedocs.io/en/latest/submit/reads/interactive.html>"""

        self.refs = '\n## References: metadata model and glossary\n\n'
        self.refs += ' * <https://ena-docs.readthedocs.io/en/latest/submit/general-guide/metadata.html>\n'
        self.refs += ' * <https://ena-docs.readthedocs.io/en/latest/submit/reads/webin-cli.html> - includes most controlled vocabularly terms\n'
        self.refs += "N.B. the Experiment Type Name is typically a combination of the overall approach and the molecular type(library_source) under investigation\n"

        self.current_expt_types = """
## Current Experiment Types

| Experiment Type | Current example | Comment |
| --- | --- | --- |
| METABARCODING | <https://www.ebi.ac.uk/ena/browser/view/SRX11512992> | |
| METAGENOMIC_SEQUENCING | <https://www.ebi.ac.uk/ena/browser/view/SRX7572557> | |
| METATRANSCRIPTOMIC | <https://www.ebi.ac.uk/ena/browser/view/DRX030329> | |
| GENOMIC | <https://www.ebi.ac.uk/ena/browser/view/SRX659582> | |
| VIRAL_RNA_GENOME | <https://www.ebi.ac.uk/ena/browser/view/ERX5705315> | |
| EXOME_SEQUENCING | <https://www.ebi.ac.uk/ena/browser/view/SRX6455994> | |
| TRANSCRIPTOMIC | <https://www.ebi.ac.uk/ena/browser/view/SRX2885726> | |
| SPATIAL_TRANSCRIPTOMIC | <https://www.ebi.ac.uk/ena/browser/view/ERX9207228> | |
| DNA_BARCODING | <https://www.ebi.ac.uk/ena/browser/view/SRX10353112> | |
| GENOTYPING | <https://www.ebi.ac.uk/ena/browser/view/SRX8470509> | |
| CHROMOSOME_CONFORMATION_CAPTURE | <https://www.ebi.ac.uk/ena/browser/view/SRX19055521> | |
| EPIGENOMIC | <https://www.ebi.ac.uk/ena/browser/view/SRX2376117> | |
| CHROMATIN_RELATED | <https://www.ebi.ac.uk/ena/browser/view/SRX6420619> | |
"""

        self.experimentTable = "## Table of most important fields in each experiment template\n\n"
        self.experimentTable += '| Checklist Group | Checklist Name | Checklist ID | Checklist Description | Checklist Version | Experiment Type Name | Experiment Type Definition | Experiment Design | Library Strategy | Library Source | Library_Selection |\n'
        self.experimentTable += '| --- | --- | --- | --- | --- | --- | --- | --- |--- | --- | -- |\n'
        ic()

    # ic(sra_obj.get_library_strategy_details())
    def addExperimentInfo(self, experimentType):
        # print(f"inside addExperimentInfo")
        ic()
        ic(experimentType.experiment_type_name)
        expt_name = experimentType.experiment_type_name
        # print(f"expt_name={expt_name}<------")
        # ic(experimentType._core_dict)
        schema_obj = experimentType.get_json_schema_obj()

        SRA_obj = schema_obj.get_SRA_obj()
        # ic(SRA_obj.get_library_strategy_details())
        lib_strat = schema_obj.get_library_strategy
        ic(lib_strat)
        #print(f"in addExperimentInfo for lib_strategy was defined----->{lib_strat}<------")
        ic(SRA_obj.get_library_strategy_detail(lib_strat))
        lib_selection = schema_obj.get_library_selection()
        ic(lib_selection)
        ic(SRA_obj.get_library_selection_detail(lib_selection))
        lib_source = schema_obj.get_library_source()
        ic(lib_source)
        self.setExperimentTableRow(experimentType, schema_obj)

        self.createExperimentTypeDoc(experimentType, schema_obj)
        # ic()
        # ic(self.experimentTable)
        # sys.exit()

    def list2md_row(self,my_list):
        md_row = "| " + " | ".join(my_list) + " |"
        return md_row
    def createExperimentTypeDoc(self, experimentType, schema_obj):
        """

        :param experimentType:
        :param schema_obj:
        :return:
        """
        print("Inside createExperimentTypeDoc")
        self.experimentTypeDoc = "# " + experimentType.experiment_type_name + "\n\n"
        checklist_specific_dict = experimentType.get_checklist_specific_dict()
        self.experimentTypeDoc += "**Description:** " + checklist_specific_dict.get("_description","sorry no description found!") + "\n\n"

        self.experimentTypeDoc += "## Introduction\n\n" \
                            "The purpose of this template is to collect high quality sequencing experiment related metadata."
        self.experimentTypeDoc += "This is an automatically generated document designed to help the populating of the JSON template for the above experiment type.\n"
        self.experimentTypeDoc += "The first table is specific to the experiment type, with the second core to all. " \
                                  "Some of the fields are:\n\n"
        self.experimentTypeDoc += "* mandatory and some optional\n"\
                "* have controlled terms or specific patterns\n" \
                "* others are free text\n\n" \
                "Some of the controlled terms may not be applicable for your particular experiment_type, they are there for completeness.\n"

        self.experimentTypeDoc += "\n## Please Note\n\n"

        self.experimentTypeDoc += "* This template **allows 1 or more experiments' metadata** to be submitted. If >1 experiments: in JSON style, please add a comma at the end of the previous record just after the closing }.\n"\
            "* **This is just guidance in one place to help you populate the template.** N.B. It may become out of date or plain wrong. So please refer to official INSDC docs in case of conflict.\n"

        #    ["platform and instrument", json.dumps(schema_obj.get_platform_instrument(), indent = 4), "Comment"]) + " |\n"

        #print(self.experimentTypeDoc)
        core_dict = schema_obj._core_dict
        #print(core_dict)

        self.experimentTypeDoc += self.getSpecificExperimentTypeTable(schema_obj, experimentType)
        self.experimentTypeDoc += self.getCoreExperimentTypeTable(schema_obj, core_dict)

        out_file = base_dir + 'docs/experiment_types/' + experimentType.experiment_type_name + '.md'
        writeString2file(self.experimentTypeDoc, out_file)
        #sys.exit()


    def getSpecificExperimentTypeDf(self, schema_obj, experimentType):
        """

        :param schema_obj:
        :param experimentType:
        :return:
        """
        ic.enable()
        # print("get_experiment_specific_dict" + json.dumps(schema_obj.get_experiment_specific_dict(), indent = 4))

        # print("get_checklist_specific_dict" + json.dumps(experimentType.get_checklist_specific_dict(), indent = 4))
        checklist_specific_dict = experimentType.get_checklist_specific_dict()

        column_names = ["Field name", "Definition", "Mandatory", "Example", "Type", "Controlled Vocab Terms", "Comment"]

        print_dict = {}
        my_dict = schema_obj.get_experiment_specific_dict()
        for field in my_dict:
            my_local = my_dict[field]
            enum = ", ".join(my_local.get("enum", ""))
            if enum == "":
                enum = ", ".join(my_local.get("pattern", ""))

            my_row = [field, my_local.get("description", ""), str(my_local.get("_required", "")), str(checklist_specific_dict[field]), my_local.get("type", ""), enum, my_local.get("_comment", "")]
            print_dict[field] = my_row

        # ic(experimentType.get_special_fields_list())
        my_dict = schema_obj.get_all_specific_fields_json_config()
        # ic(my_dict)
        for field in my_dict:
            my_local = my_dict[field]
            enum = ", ".join(my_local.get("enum", ""))
            if enum == "":
                enum = ", ".join(my_local.get("pattern", ""))
            my_row = [field, my_local.get("description", ""), str(my_local.get("_required", "")), "", my_local.get("type", ""), enum, my_local.get("_comment", "")]
            print_dict[field] = my_row

        df = pd.DataFrame.from_dict(print_dict, orient = 'index', columns = column_names)
        # df = pd.df = pd.DataFrame.from_dict(print_dict, orient = 'index', columns = [val_col_name]).from_dict(print_dict, orient = 'index', columns = [val_col_name])

        return df
    def getSpecificExperimentTypeTable(self, schema_obj, experimentType):
        """

        :param schema_obj:
        :param experimentType:
        :return:
        """
        self.specific_experimentTypeDoc = ""
        my_dict = schema_obj.get_experiment_specific_dict()
        self.specific_experimentTypeDoc += "\n## " + experimentType.experiment_type_name + " Experiment Specific Fields\n\n"

        df = self.getSpecificExperimentTypeDf( schema_obj, experimentType)
        self.specific_experimentTypeDoc += df.to_markdown()

        return self.specific_experimentTypeDoc

    def getCoreExperimentTypeDf(self, schema_obj, core_dict):
        column_names = ["Field name", "Definition", "Mandatory", "Example", "Controlled Vocab Terms", "Comment"]
        # print(list(core_dict))
        # print(list(core_dict["coreFields"]))
        # print(core_dict["coreFields"]["library_layout"])
        print_dict = {}
        for coreField in core_dict["coreFields"]:
            if not coreField.startswith("_"):
                # print(f"coreField={coreField}")
                my_local = core_dict["coreFields"][coreField]
                enum = ", ".join(my_local.get("enum", ""))
                if enum == "":
                    enum = my_local.get("pattern", "")
                    enum = enum.replace("|","\|")
                my_list = [coreField, my_local.get("description", ""), str(my_local.get("_required", "N.A.")), str(my_local.get("default", "")), enum, my_local.get("_comment", "")]

                print_dict[coreField] = my_list

        df = pd.DataFrame.from_dict(print_dict, orient = 'index', columns = column_names)
        return df

    def getCoreExperimentTypeTable(self, schema_obj, core_dict):
        self.core_experimentTypeDoc = ""
        self.core_experimentTypeDoc += "\n\n## Core Fields\n\n"
        self.getCoreExperimentTypeDf(schema_obj, core_dict)
        df = self.getCoreExperimentTypeDf( schema_obj, core_dict)
        ic(df)
        self.core_experimentTypeDoc += df.to_markdown(index = False)
        self.core_experimentTypeDoc += "\n\n"

        # print(self.core_experimentTypeDoc)
        return self.core_experimentTypeDoc

    def setExperimentTableRow(self,experimentType, schema_obj):
        self.experimentTable += '| '
        self.experimentTable += schema_obj.get_checklist_group() + ' | '
        self.experimentTable += schema_obj.get_checklist_name() + ' | '
        self.experimentTable += schema_obj.get_checklist_id() + ' | '
        self.experimentTable += schema_obj.get_checklist_description() + ' | '
        self.experimentTable += schema_obj.get_checklist_version() + ' | '
        self.experimentTable += experimentType.experiment_type_name + ' | '
        self.experimentTable += schema_obj.get_experiment_type_definition() + ' | '
        self.experimentTable += schema_obj.get_experiment_design_description() + ' | '
        self.experimentTable += schema_obj.get_library_strategy + ' | '
        self.experimentTable += schema_obj.get_library_source() + ' | '
        self.experimentTable += schema_obj.get_library_selection() + ' |'
        self.experimentTable += '\n'


    def print_checklist_doc(self):
        output = []
        output.append(self.title)
        output.append(self.intro)
        output.append(self.overall)
        output.append(self.current_expt_types)
        output.append(self.experimentTable)
        outstring = '\n'.join(output)
        # ic(outstring)
        writeString2file(outstring, base_dir + '/docs/ExperimentChecklistTables.md')
        return outstring

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
        self._specific_json_config = ""
        self.set_experiment_specific_dict(experiment_type_obj.get_checklist_specific_dict())
        self.set_platform_instrument()
        experiment_type_obj.set_json_schema_obj(self)
        ic("just set_json_schema_obj")

    def get_experiment_type_obj(self):
        return self._experimentType
    def get_SRA_obj(self):
        if hasattr(self, 'SRA_obj'):
            ic()
        else:
            #ic.disable()
            sra_xml_obj = get_SRA_XML_baseline()
            self.SRA_obj = sra_xml_obj
            #ic.enable()
        return self.SRA_obj

    def set_platform_instrument(self):
        """
         gets the platform and instrument JSON configuration ultimately from the experiment_sra_xml
         e.g. {'BGISEQ': ['BGISEQ-500', 'MGISEQ-2000RS', 'BGISEQ-50'],
                'DNBSEQ': ['DNBSEQ-G50','DNBSEQ-G400 FAST','DNBSEQ-T7', 'unspecified','DNBSEQ-G400']
              }
        :return:
        """
        ic()
        sra_xml_obj = self.get_SRA_obj()
        self.platform_instrument = sra_xml_obj.get_platform()
        # schema_core_dict = {"properties": self.get_core_fields_dict()}
        # properties instrument_platform enum LIST
        #ic(self._core_dict['coreFields'])
        self._core_dict['coreFields']["instrument_platform"]["enum"] = sra_xml_obj.get_platform_list()
        # properties instrument_model enum LIST
        self._core_dict['coreFields']["instrument_model"]["enum"] = sra_xml_obj.get_instrument_list()
        self._core_dict['coreFields']["library_source"]["enum"] = sra_xml_obj.get_library_source_list()
        self._core_dict['coreFields']["library_selection"]["enum"] = sra_xml_obj.get_library_selection_list()
        self._core_dict['coreFields']["library_strategy"]["enum"] = sra_xml_obj.get_library_strategy_list()
        ic(self._core_dict.keys())
        #target_loci

        self.set_platform_instrument_rules()

    def get_platform_instrument(self):
        # dict of platform as keys and an array of instruments for each platform
        return self.platform_instrument

    def get_experiment_type_name(self):
        return self.experiment_type_name

    def get_core_dict(self):
        return self._core_dict

    def get_core_fields_dict(self):
        """get_core_fields_dict
        This already has the JSON schema attributes
        """
        return self._core_dict['coreFields']

    def get_core_fields_dict_keylist(self):
        """

        :return: all the CORE terms
        """
        return list(self._core_dict['coreFields'].keys())

    def get_properties_required_term_list(self):
        """
        gets properties required terms ,does not get allOF terms

        :return: list of required_term
        """
        ic()
        required_terms = []
        for term in self.get_core_fields_dict_keylist():
            if "_comment" in term:
                ic(f"exclude: {term}")
            else:
                required_terms.append(term)
        #ic(required_terms)
        return required_terms

    def get_experiment_specific_dict_keylist(self):
        """

        :return: all the experiment_specific terms
        """
        my_dict = self.get_experiment_specific_dict()
        return list(my_dict.keys())

    def get_allof_required_term_list(self):
        """
        gets allOf terms, and returns those
         that need to be required as list.
         By default, all are required.
        (does not get other properties terms)

        :return: list of required_term
        """
        required_terms = []
        for term in self.get_experiment_specific_dict_keylist():
            if "_comment" in term:
                ic(f"exclude: {term}")
            else:
                required_terms.append(term)
        ic.enable()
        experiment_type_obj = self.get_experiment_type_obj()
        special_dict = experiment_type_obj.get_special_dict()
        ic(special_dict)
        for term in list(special_dict.keys()):
            ic(term)
            if "_comment" in term:
                ic(f"exclude: {term}")
            else:
                required_terms.append(term)
        print(required_terms)

        # ic.disable()
        # sys.exit()
        return required_terms

    def set_platform_instrument_rules(self):
        """
           set_instrument_platform_rules as instruments specific to platform, except for "unspecified"
        :return:
        """
        pi = self.get_platform_instrument()
        pi_rules = []
        count = 0

        #ic(self._core_dict['coreRules'])

        for platform in pi:
            #ic(platform)
            pi_rule = {'if': {'properties': {'instrument_platform': {'const': ""}}}}
            pi_rule['if']['properties']['instrument_platform']['const'] = platform
            pi_rule['then'] = {'properties': {'instrument': {'enum': ""}}}
            pi_rule['then']['properties']['instrument']['enum'] = pi[platform]
            #ic(pi_rule)
            pi_rules.append(pi_rule)
            count += 1
        #ic(pi_rules)
        self._core_dict['coreRules'].extend(pi_rules)
        #ic(self._core_dict['coreRules'])
        #print(self._core_dict['coreRules'])


    def get_instrument_platform_rules(self):
        pass

    def get_core_rules_list(self):
        """get_core_fields_dict

        """
        #ic(self._core_dict['coreRules'])

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
        ic()
        sra_xml_obj = self.get_SRA_obj()
        # ic(experiment_specific_dict)
        all_specific_dict = self.get_all_specific_fields_json_config()
        my_specific_json_config = {}
        for field in experiment_specific_dict:
            if field in all_specific_dict:
                my_specific_json_config[field] = all_specific_dict[field]
                my_specific_json_config[field]["default"] = experiment_specific_dict[field]
                my_specific_json_config[field]["_example"] = my_specific_json_config[field]["default"]
            else:
                ic("WARNING: need to add json config for ", field)
        # ic(my_specific_json_config)

        #filling in some enums from the SRA_experiment object
        if my_specific_json_config.get('target_loci'):
            #ic()
            #ic(my_specific_json_config.get('target_loci'))
            #ic(sra_xml_obj.get_targetted_loci_list())
            my_specific_json_config['target_loci']['enum'] = sra_xml_obj.get_targetted_loci_list()
            #exit()
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
        ic("get_json_schema")


        def dict2objects(my_dict):
            """
            create a list of JSON style objects
            :param my_dict:
            :return:
            """
            rtn_dict = []  # {"_comment3": {"description": "some", "type": "string"}}
            # ic(rtn_dict)
            for term in my_dict:
                # ic(term)
                # ic(my_dict[term])
                data = {term: my_dict[term]}
                rtn_dict.append(data)
                # ic(rtn_dict)
            return rtn_dict

        if hasattr(self, "_schema_dict"):
            ic("already has _schema_dict")
        else:
            ic("=" * 80)
            ic("need to create a schema")
            schema_core_dict = {"properties": self.get_core_fields_dict()}
            # properties instrument_platform enum LIST
            # properties instrument_model enum LIST
            schema_rules_dict = {"allOf": self.get_core_rules_list()}
            # experiment_type_specific_dict = {"allOf": [self.get_experiment_specific_dict()]}
            # experiment_specific_dict = self.get_experiment_specific_dict()
            experiment_type_specific_dict = {"allOf": dict2objects(self.get_experiment_specific_dict())}
            #ic(experiment_type_specific_dict)
            # cl_metadata_dict["checklists"] = self.get_schema_metadata()
            """N.B. this does a deep merge of the dictionaries, most other methods did not..."""
            ic()

            self._schema_dict = merge(schema_core_dict, self.get_schema_metadata(),
                                      experiment_type_specific_dict)
            #ic(schema_rules_dict)
            #ic(schema_rules_dict['allOf'])
            # rules = schema_rules_dict['allOf'].pop(0)    # tried, but it would not merge
            for rule in schema_rules_dict['allOf']:
                #ic(rule)
                self._schema_dict['allOf'].append(rule)
            ic()
            self._schema_dict['allOf'].append({"required": self.get_allof_required_term_list()})
            self._schema_dict["required"] = self.get_properties_required_term_list()
            #ic(self._schema_dict['allOf'])
            # print("get the array of")
            # ic(schema_dict)
            # **json_schema_dict}
            return self._schema_dict

            def list2required(term_list):
                """

                :param term_list:
                :return: term_list[] =
                """
                ic(term_list)
                tmp = {"required": term_list}
                return tmp

            schema_dict["allOf"].append(list2required(self.get_allof_required_term_list()))
            schema_dict["required"] = self.get_properties_required_term_list()
            self._schema_dict = schema_dict
            #ic(schema_dict)
        #ic(self._schema_dict)

        return self._schema_dict

    def print_json_schema(self):
        """ printout_json_schema to a JSON file
        params:
        return: json too

        """
        ic()
        data_loc_dict = get_data_locations()
        json_schema_dict = self.get_json_schema()
        # ic(json_schema_dict)
        outfileName = data_loc_dict["schema_dir"] + self.experiment_type_name + '_schema.json'
        ic(outfileName)

        """Create a list as top level """
        # my_list = [json_schema_dict]
        json_object = json.dumps(json_schema_dict, indent = 4, sort_keys = True)
        with open(outfileName, "w") as outfile:
            outfile.write(json_object)
        return json_object

    def get_checklist_name(self):
        experiment_type_obj = self.get_experiment_type_obj()
        my_dict = experiment_type_obj.get_all_dict()
        # ic(my_dict)
        ic(my_dict['checklist_name'])
        return my_dict['checklist_name']

    def get_checklist_id(self):
        experiment_type_obj = self.get_experiment_type_obj()
        my_dict = experiment_type_obj.get_all_dict()
        return my_dict['checklist_id']

    def get_checklist_version(self):
        experiment_type_obj = self.get_experiment_type_obj()
        my_dict = experiment_type_obj.get_all_dict()
        return my_dict['checklist_version']

    def get_experiment_type_definition(self):
        experiment_type_obj = self.get_experiment_type_obj()
        my_dict = experiment_type_obj.get_all_dict()
        return my_dict['experiment_type_definition'].replace("\n"," ")

    def get_experiment_design_description(self):
        experiment_type_obj = self.get_experiment_type_obj()
        my_dict = experiment_type_obj.get_all_dict()
        # ic(my_dict['checklist_name'])
        return my_dict.get("design_description", "")

    def get_checklist_description(self):
        experiment_type_obj = self.get_experiment_type_obj()
        my_dict = experiment_type_obj.get_all_dict()
        return my_dict['_description']

    def get_checklist_group(self):
        experiment_type_obj = self.get_experiment_type_obj()
        my_dict = experiment_type_obj.get_all_dict()
        return my_dict['checklist_group']

    def get_library_source(self):
        """

        :return: term
        """
        experiment_type_obj = self.get_experiment_type_obj()
        my_dict = experiment_type_obj.get_all_dict()
        return my_dict['library_source']

    @property
    def get_library_strategy(self):
        """
        get_library_strategy will only return if field defined!!! Which will ofter not be true, so returns "" in those cases
        :return: term
        """
        # print("inside schema get_library_strategy")
        experiment_type_obj = self.get_experiment_type_obj()
        my_dict = experiment_type_obj.get_all_dict()
        # stwing = json.dumps(my_dict, indent=4)
        # print(f"my_dict={stwing}")
        # print(my_dict['library_strategy'])
        ic(my_dict['library_strategy'])
        return my_dict.get('library_strategy',"")

    def get_library_selection(self):
        """

        :return: term
        """
        experiment_type_obj = self.get_experiment_type_obj()
        my_dict = experiment_type_obj.get_all_dict()
        ic(my_dict['library_selection'])
        return my_dict['library_selection']


class ExperimentType:
    """ ExperimentType object
    for handling generating the Json user checklist for each ExperimentType
    params:
        in: experiment_type string
        initially very minimal, mainly gets set up in get_and_process_fields()
    """

    def __init__(self, experiment_type_name):
        ic("inside ExperimentType init class")
        self._json_schema_obj = None
        self._special_dict = None
        self._special_fields_list = None
        self._core_dict = None
        self._checklist_dict = None
        self._core_dict_default_values = None
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
        tmp = self._checklist_dict
        ic(tmp.keys())
        return self._checklist_dict

    def set_special_dict(self, special_dict):
        self._special_dict = special_dict

    def get_special_dict(self):
        tmp = self._special_dict
        ic(tmp.keys())
        return self._special_dict

    def get_core_dict(self):
        ic()
        tmp = self._core_dict
        ic(tmp.keys())
        return self._core_dict

    def set_core_dict(self, core_dict):
        self._core_dict = core_dict

    def set_core_dict_default(self, core_dict_default):
        self._core_dict_default_values = core_dict_default

    def get_core_dict_default(self):
        return self._core_dict_default_values

    def get_all_dict(self):
        if hasattr(self, '_all_dict'):
            return self._all_dict
        else:
            ic()
            all_dict = {**self.get_checklist_specific_dict(), **self.get_core_dict(), **self.get_special_dict()}
            # ic(self.get_checklist_specific_dict())
            # ic(self.get_core_dict())
            # ic(self.get_special_dict())
            all_dict = self.clean_all_dict(all_dict)
            self._all_dict = all_dict
        return all_dict

    def clean_all_dict(self, all_dict):
        """clean_all_dict
        Sometimes the checklist specific was getting overwritten, so forcing this"""
        checklist_specific_dict = self.get_checklist_specific_dict()
        for field in checklist_specific_dict:
            ic(field, checklist_specific_dict[field])
            if checklist_specific_dict != "":
                all_dict[field] = checklist_specific_dict[field]
        return all_dict

    def get_all_dict_default(self):
        ic()
        all_dict = {**self.get_checklist_specific_dict(), **self.get_core_dict_default(), **self.get_special_dict()}
        all_dict = self.clean_all_dict(all_dict)

        return all_dict
    def get_ExperimentTypeObj_values(self):
        """

        :return:
        """
        ic()
        return self.get_all_dict()

    def get_experiment_type(self):
        if hasattr(self, 'experiment_type'):
            return self.experiment_type
        checklist_dict = self.get_all_dict()
        self.experiment_type = checklist_dict['experiment_type']
        return self.experiment_type

    def print_checklist_json(self):
        """

        :param checklist_dict:
        :return:
        """
        data_loc_dict = get_data_locations()
        checklist_dict = self.get_all_dict()
        # ic(checklist_dict)
        outfileName = data_loc_dict["output_dir"] + checklist_dict['experiment_type'] + '.json'
        json_object = json.dumps(checklist_dict, indent = 4, sort_keys = True)
        with open(outfileName, "w") as outfile:
            outfile.write(json_object)
        ic(outfileName)

    def get_checklist_as_df(self):
        if hasattr(self, 'checklist_as_df'):
            return self.checklist_as_df

        checklist_dict = self.get_all_dict()
        print_dict = {}
        for key in checklist_dict.keys():
            if key in ['experiment_attribute', 'pcr_primers', 'sequence_related']:
                if key in ['sequence_related', 'pcr_primers', 'experiment_attribute']:
                    for sub_key in checklist_dict[key]:
                        add_key = key + ":" + sub_key
                        print_dict[add_key] = [str(checklist_dict[key][sub_key])]
                        # print(f"{add_key} {print_dict[add_key]}")
                else:  #may wish to do something more adnvaced
                    print_dict[key] = [checklist_dict[key]]
            else:
                print_dict[key] = [checklist_dict[key]]
        # ic(print_dict)
        # df = pd.DataFrame.from_dict(print_dict, orient='index', columns=['KEY', 'SUB'])
        field_col_name = checklist_dict['experiment_type']
        val_col_name = 'value for ' + checklist_dict['experiment_type']
        df = pd.DataFrame.from_dict(print_dict, orient = 'index', columns = [val_col_name])
        df[field_col_name] = df.index
        self.checklist_as_df = df[[field_col_name, val_col_name]].sort_index()
        # ic(self.checklist_as_df)
        return self.checklist_as_df


    def print_checklist_xlsx(self):
        """

        :param checklist_dict:
        :return:
        """
        data_loc_dict = get_data_locations()

        outfileName = data_loc_dict["output_xlsx_dir"] + self.get_experiment_type() + '.xlsx'
        df = self.get_checklist_as_df()
        df.to_excel(outfileName, index = False)
        ic(outfileName)

    def print_checklist(self):
        """
        params:

        """
        ic()
        self.print_checklist_xlsx()
        self.print_checklist_json()

    #
    # def print_test_checklist(self):
    #     """ print_test_checklist
    #     as print_checklist, but uses the default values
    #     params:
    #     deprecated
    #     """
    #     ic()
    #     data_loc_dict = get_data_locations()
    #
    #     all_checklist_dict = self.get_all_dict_default()
    #     # ic(all_checklist_dict)
    #
    #     outfileName = data_loc_dict["output_test_dir"] + all_checklist_dict['experiment_type'] + '.json'
    #     ic(outfileName)
    #
    #     my_list = all_checklist_dict
    #     json_object = json.dumps(my_list, indent = 4, sort_keys = True)
    #     with open(outfileName, "w") as outfile:
    #         outfile.write(json_object)
    #     return


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
    ic()
    # ic(config_data['coreFields'])
    coreDict = {}
    coreDictDefaultVal = {}
    for field in config_data['coreFields']:
        if "_comment" in field:
            continue
        # ic('+' * 80)
        # ic(field)
        # if field not in ["library_source"]:
        #    continue
        if isinstance(config_data['coreFields'][field], dict):
            ic(field, " in config_data", config_data['coreFields'][field])
            if config_data['coreFields'][field]['type'] == 'number':
                # ic(config_data['coreFields'][field])
                coreDict[field] = config_data['coreFields'][field]['default']
                """as they are numeric, the JSON wants a number not a string"""
            else:
                coreDict[field] = ""

            if (coreDict[field] != "") and ("default" in config_data['coreFields'][field]):
                coreDictDefaultVal[field] = coreDict[field]
                ic("first if:", coreDictDefaultVal[field])
            elif "default" in config_data['coreFields'][field]:
                # ic(config_data['coreFields'][field]['default'])
                coreDictDefaultVal[field] = config_data['coreFields'][field]['default']
                ic("el if:", coreDictDefaultVal[field])
            else:
                coreDictDefaultVal[field] = ""
                ic("else :", coreDictDefaultVal[field])
            # ic(type(config_data['coreFields'][i]))
            # ic("dict: " + str(config_data['coreFields'][i]))
        else:
            ic(field, " not in config_data['coreFields']")
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
    ic.enable()
    for jsonKey in special_keys:
        ic(jsonKey)
        if jsonKey in config_data:
            ic(config_data[jsonKey])
            local_dict = {**local_dict, **config_data[jsonKey]}
            ic(local_dict)
        else:
            ic('WARN "special" key does not exist: "' + jsonKey +
               '" please check the config data in the input JSON file' + ' for *_fields')
    experiment_type.set_special_dict(local_dict)
    # sys.exit()
    return


def process_and_get_fields(config_data):
    """ method to get all the fields and values needed for a particular checklist as JSON
        in: config_data
        rtn: Dict of experimentType objects
    """
    ic()
    (coreDict, coreDictDefaultVal) = get_core_dict(config_data)
    ic(coreDict)
    ic(coreDictDefaultVal)
    expt_objects_dict = {}
    for e_type_slice in config_data['experimentTypes']:
        ic(e_type_slice)
        # create a dictionary of ExperimentType objects index on the name of the experimentType
        experimentType = ExperimentType(e_type_slice["experiment_type"])
        ic(experimentType)
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
        ic()
        # ic(experimentType.print_ExperimentTypeObj())
    return expt_objects_dict

def get_data_locations():
    """ get_data_locations
    params:
        rtn: data_loc_dict
    """
    data_loc_dict = {"base_dir": "/Users/woollard/projects/easi-genomics/ExperimentChecklist/"}
    data_dir = data_loc_dict["base_dir"] + "data/"
    data_loc_dict["input_dir"] = data_dir + "input/"
    data_loc_dict["output_dir"] = data_dir + "output/"
    data_loc_dict["output_xlsx_dir"] = data_dir + "output_xlsx/"
    data_loc_dict["output_test_dir"] = data_dir + "output_test/"
    data_loc_dict["schema_dir"] = data_dir + "schema/"
    return data_loc_dict

def read_config(debug_status):
    """ readConfig
    reads the master JSON file
    This file provides all the JSON data fields etc. that are used to build the different experiment templates
    params:
        rtn: JSON
    """
    ic(debug_status)

    data_loc_dict = get_data_locations()
    if not debug_status:
        filename = data_loc_dict["input_dir"] + "ExperimentChecklistIn.json"
    else:
        filename = data_loc_dict["input_dir"] + "test_ExperimentChecklistIn.json"
    print(filename)
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
    combined_cl_df = pd.DataFrame()
    for experiment_type_name in expt_objects:
        ic(experiment_type_name)
        experimentType = expt_objects[experiment_type_name]
        experimentType.print_checklist()
        # experimentType.print_test_checklist()
        expt_cl_df = experimentType.get_checklist_as_df()
        ic(len(expt_cl_df))
        sys.exit()

    # sys.exit()

def create_schema_objects(expt_objects, config_data):
    """ create_schema_objects
        params:
        in: expt_objects, config_data
        rtn: schema_objects_dict
    """
    ic()
    print("inside create_schema_objects")
    schema_objects = {}

    for experiment_type_name in expt_objects:
        ic(experiment_type_name)
        experimentType: object = expt_objects[experiment_type_name]
        schema_objects[experiment_type_name] = ExperimentTypeJsonSchema(experimentType, config_data)
        schema_obj = schema_objects[experiment_type_name]
        experimentType.set_json_schema_obj(schema_obj)
        ic(schema_obj)
        schema_obj.print_json_schema()
    return schema_objects

def print_all_checklist_json_schemas(expt_objects):
    ic("-" * 100)
    ic()
    for experiment_type_name in expt_objects:
        ic(experiment_type_name)
        experimentType = expt_objects[experiment_type_name]
        ic(experimentType)
        schema_obj = experimentType.get_json_schema_obj()
        # ic(schema_obj)
        # print(schema_obj.experiment_type_name)
        # print(schema_obj.get_core_fields_dict())
        # print(schema_obj.get_core_rules_list())
        # print(schema_obj.print_json_schema())
        ic()
        experimentType.print_ExperimentTypeObj()

def main():
    ic()
    debug_status = True
    debug_status = False
    schema_json_file = '/Users/woollard/projects/easi-genomics/ExperimentChecklist/data/testing/METABARCODING_schema.json'
    # json_obj = file2json(schema_json_file)
    # print(json_obj)

    checklist_doc = ChecklistDoc()
    config_data = read_config(debug_status)
    expt_objects_dict = process_and_get_fields(config_data)
    ic(expt_objects_dict)

    print("## Create expt_objects_dict for each experiment:")
    for experiment_type_name in expt_objects_dict:
        # if experiment_type_name != 'TEST_type':
        #     continue
        #print(experiment_type_name)
        ic(experiment_type_name)
        experimentType = expt_objects_dict[experiment_type_name]
        #ic(experimentType.get_ExperimentTypeObj_values())
    ic()

    #print_all_checklists(expt_objects_dict)
    #
    #print_all_checklist_json_schemas(expt_objects_dict)
    schema_obj_dict = create_schema_objects(expt_objects_dict, config_data)
    print("-" * 100)
    print(f"debug_status = {debug_status}")
    for experiment_type_name in schema_obj_dict:
        ic()
        ic(experiment_type_name)
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


if __name__ == '__main__':
    main()
