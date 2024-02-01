
from icecream import ic
import re
import pandas as pd
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
from ExperimentUtils import get_data_locations
import json
import pandas as pd
import sys

class ExperimentType:
    """ ExperimentType object
    for handling generating the Json user checklist for each ExperimentType
    params:
        in: experiment_type string
        initially very minimal, mainly gets set up in get_and_process_fields()
    """

    def __init__(self, experiment_type_name):
        # ic(f"inside ExperimentType init class for {experiment_type_name}")
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
        if self._json_schema_obj == None:
            print("ERROR: self._json_schema_obj has not be set in ExperimentType Object")
            sys.exit()
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
        # ic(tmp.keys())
        return self._checklist_dict

    def set_special_dict(self, special_dict):
        self._special_dict = special_dict

    def get_special_dict(self):
        tmp = self._special_dict
        # ic(tmp.keys())
        return self._special_dict

    def get_core_dict(self):
        tmp = self._core_dict
        # ic(tmp.keys())
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
            # ic(field, checklist_specific_dict[field])
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
        :return: outfileName
        """
        data_loc_dict = get_data_locations()
        checklist_dict = self.get_all_dict()
        # ic(checklist_dict)
        outfileName = data_loc_dict["output_dir"] + checklist_dict['experiment_type'] + '.json'
        json_object = json.dumps(checklist_dict, indent = 4, sort_keys = True)
        with open(outfileName, "w") as outfile:
            outfile.write(json_object)
        return outfileName

    def getSpecificExperimentTypeDict(self):
        """

        :return: et_specific_dict
        """
        schema_obj = self.get_json_schema_obj()
        core_dict = self.get_core_dict()
        ic(core_dict)
        #sys.exit()
        # my_dict = schema_obj.get_experiment_specific_dict()
        # ic(my_dict)
        # self.specificExperimentTypeDf = self.experimentTypeMetaDataDf(my_dict)
        # ic(self.specificExperimentTypeDf)
        # sys.exit()
        # ic("---------ALL SPECIFIC FIELDS----------------")
        all_specific_dict = schema_obj.get_experiment_specific_dict()
        # ic(all_specific_dict)
        checklist_specific_dict = self.get_checklist_specific_dict()
        ic(checklist_specific_dict)
        ic(all_specific_dict["checklist_version"])
        et_specific_dict = {}
        missing_field_list = []
        for field_in_et in checklist_specific_dict:
            if field_in_et in all_specific_dict:
                et_specific_dict[field_in_et] = all_specific_dict[field_in_et]
                et_specific_dict[field_in_et]['_default'] = checklist_specific_dict[field_in_et]
                et_specific_dict[field_in_et]['_example'] = et_specific_dict[field_in_et]['_default']
            else:
                ic(field_in_et)
                missing_field_list.append(field_in_et)
                if field_in_et not in core_dict:
                    et_specific_dict[field_in_et] = {"_description": checklist_specific_dict[field_in_et]}
        if missing_field_list:
            print(f"INFO: for {self.experiment_type_name} these are not in the schema specific field list {missing_field_list}")

        return et_specific_dict


    def getSpecificExperimentTypeDf(self):
        """

        :return:
        """
        # ic()
        # ic(self.experiment_type_name)
        if hasattr(self, 'specificExperimentTypeDf'):
            return self.specificExperimentTypeDf

        self.specificExperimentTypeDf = self.experimentTypeMetaDataDf("specific")
        # ic(self.specificExperimentTypeDf)

        return self.specificExperimentTypeDf


    def getTotalDetailExperimentTypeDf(self):
        ic()
        print("-----------------------------------------------------------------------")
        specificExperimentTypeDf = self.getSpecificExperimentTypeDf()
        ic(specificExperimentTypeDf['Field name'])
        print(specificExperimentTypeDf.head(2).to_markdown())
        print("-----------------------------------------------------------------------")
        coreExperimentTypeDf = self.getCoreExperimentTypeDf()
        print(coreExperimentTypeDf.head(2).to_markdown())
        self._totalDetailExperimentTypeDf = pd.concat([specificExperimentTypeDf, coreExperimentTypeDf, ])
        print(self._totalDetailExperimentTypeDf.head(20).to_markdown())

        return self._totalDetailExperimentTypeDf

    def experimentTypeMetaDataDf(self, schemaType):
        """
        :param schemaType: one of "core" or "specific"
        :return: df
        """
        ic()
        ic(schemaType)
        if schemaType == "core":
            schema_core_dict = self.get_schema_core_fields_dict()
        elif schemaType == "specific":
            schema_core_dict = self.getSpecificExperimentTypeDict()
        else:
            ic()
            print(f"ERROR: {schemaType} is not known")
            sys.exit()

        #if hasattr(self, '_experimentTypeMetaDataDf'):
        #    return self._experimentTypeMetaDataDf
        ic.disable()
        ic()
        column_names = ["Field name", "Specificity", "Definition", "Mandatory", "Example", "Type",
                        "Controlled Vocab Terms", "Comment"]
        print_dict = {}
        specificity = schemaType
        for coreField in schema_core_dict:
            ic(coreField)
            if not coreField.startswith("_"):
                # print(f"coreField={coreField}")
                my_local = schema_core_dict[coreField]
                ic(my_local)
                enum = ", ".join(my_local.get("enum", ""))
                if enum == "":
                    enum = my_local.get("pattern", "")
                    enum = enum.replace("|","\|")
                example = str(my_local.get("_example", ""))
                if example == "":
                    ic("Example is blank so using default")
                    example = str(my_local.get("default", ""))
                my_list = [coreField, specificity, my_local.get("description", ""),
                           str(my_local.get("_required", "N.A.")), example,
                           str(my_local.get("type", "")),  enum,
                            my_local.get("_comment", "")]
                print_dict[coreField] = my_list
        #ic(print_dict)
        df = pd.DataFrame.from_dict(print_dict, orient = 'index', columns = column_names)
        ic.enable()
        # ic(df.head())
        self._experimentTypeMetaDataDf = df
        return self._experimentTypeMetaDataDf

    def get_schema_core_fields_dict(self):
        schema_obj = self.get_json_schema_obj()
        schema_core_dict = schema_obj.get_core_fields_dict()
        return(schema_core_dict)

    def getCoreExperimentTypeDf(self):
        ic()
        ic.enable()
        if hasattr(self, 'coreExperimentTypeDf'):
            return self.coreExperimentTypeDf
        # schema_obj = self.get_json_schema_obj()
        # schema_core_dict = schema_obj.get_core_fields_dict()
        schema_core_dict = self.get_schema_core_fields_dict()

        self.coreExperimentTypeDf = self.experimentTypeMetaDataDf("core")
        ic.enable()
        df = self.coreExperimentTypeDf
        # ic(df)
        #ic(df['study_id'])
        #sys.exit()
        return self.coreExperimentTypeDf

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


    def print_checklist_summary_xlsx(self):
        """

        :param checklist_dict:
        :return: outfileName
        """
        data_loc_dict = get_data_locations()
        df = self.get_checklist_as_df()

        outfileName = data_loc_dict["output_xlsx_dir"] + "summary_" + self.get_experiment_type() + '.xlsx'
        df.to_excel(outfileName, index = False)

        outfileName = data_loc_dict["output_md_dir"] + "summary_" + self.get_experiment_type() + '.md'
        df.to_markdown(outfileName, index = False)
        return outfileName

    def print_checklist_detail_xlsx(self):
        """

        :param checklist_dict:
        :return: outfileName
        """
        data_loc_dict = get_data_locations()

        outfileName = data_loc_dict["output_xlsx_dir"] + self.get_experiment_type() + '.xlsx'

        total_df = self.getTotalDetailExperimentTypeDf()
        ic(total_df.head())
        total_df.to_excel(outfileName, index = False)

        outfileName = data_loc_dict["output_md_dir"] + self.get_experiment_type() + '.md'
        total_df.to_markdown(outfileName, index = False)

        return outfileName

    def print_checklist_specific_xlsx(self):
        data_loc_dict = get_data_locations()
        outfileName = data_loc_dict['output_xlsx_dir'] + "specific_" + self.get_experiment_type() + ".xlsx"
        # ic(experimentType.getSpecificExperimentTypeDf())
        self.getSpecificExperimentTypeDf().to_excel(outfileName, index = False)
        return outfileName

    def print_checklist(self):
        """
        params:

        """
        ic()
        ic(self.print_checklist_detail_xlsx())
        ic(self.print_checklist_summary_xlsx())
        ic(self.print_checklist_json())
        ic(self.print_checklist_specific_xlsx())

# -------------------
def process_and_get_fields2expt_type_obj_dict(config_data):
    """ method to get all the fields and values needed for a particular checklist as JSON
        in: config_data
        rtn: Dict of experimentType objects, keyed off the experiment type name
    """
    # ic()
    (coreDict, coreDictDefaultVal) = get_core_dict(config_data)
    expt_objects_dict = {}
    for e_type_slice in config_data['experimentTypes']:
        # ic()
        # ic(e_type_slice["experiment_type"])
        # ic(e_type_slice)
        # create a dictionary of ExperimentType objects index on the name of the experimentType
        my_json_str = e_type_slice["experiment_type"]
        experimentType = ExperimentType(my_json_str)
        # ic(experimentType.experiment_type_name)
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
    # print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    # metabarcoding_eT = expt_objects_dict['METABARCODING']
    # ic(metabarcoding_eT.get_checklist_specific_dict())
    # print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    # metabarcoding_eT = expt_objects_dict['GENOMIC']
    # ic(metabarcoding_eT.get_checklist_specific_dict())

    return expt_objects_dict

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
            local_dict = {**local_dict, **config_data[jsonKey]}
        else:
            print('WARN "special" key does not exist: "' + jsonKey +
               '" please check the config data in the input JSON file' + ' for *_fields')
    experiment_type.set_special_dict(local_dict)
    return

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
                coreDict[field] = config_data['coreFields'][field]['_default']
                """as they are numeric, the JSON wants a number not a string"""
            else:
                coreDict[field] = ""

            if (coreDict[field] != "") and ("default" in config_data['coreFields'][field]):
                coreDictDefaultVal[field] = coreDict[field]
                # ic("first if:", coreDictDefaultVal[field])
            elif "default" in config_data['coreFields'][field]:
                # ic(config_data['coreFields'][field]['_default'])
                coreDictDefaultVal[field] = config_data['coreFields'][field]['_default']
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


