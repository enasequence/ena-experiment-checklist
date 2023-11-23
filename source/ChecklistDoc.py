
from icecream import ic
import pandas as pd
from ExperimentUtils import get_data_locations, writeString2file, get_base_dir
from ExperimentType import ExperimentType
#from schema_obj import get_sra_obj
class ChecklistDoc:
    """
    Create md documentation for the experiments type checklists

    """
    from icecream import ic

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
        data_loc_dict = get_data_locations()
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
        out_file = data_loc_dict["base_dir"] + 'docs/experiment_types/' + experimentType.experiment_type_name + '.md'
        writeString2file(self.experimentTypeDoc, out_file)


    def getSpecificExperimentTypeDf(self, schema_obj, experimentType):
        """

        :param schema_obj:
        :param experimentType:
        :return:
        """
        ### TODO: refactor the whole class to use functions from ExperimentType object.
        ### N.B. This is essentially a mirror of the function of th same name in ExperimentType
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
        ### TODO: refactor the whole class to use functions from ExperimentType object.
        ### N.B. This is essentially a mirror of the function of th same name in ExperimentType
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
        ic()
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
        out_file = str(get_base_dir()) + '/docs/ExperimentChecklistTables.md'
        ic(out_file)
        writeString2file(outstring, out_file)
        return outstring
