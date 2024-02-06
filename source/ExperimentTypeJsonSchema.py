from mergedeep import merge
from extract_experiment_XML_vals import get_SRA_XML_baseline
from ExperimentUtils import get_data_locations, read_config
import json
from icecream import ic
import sys

class ExperimentTypeJsonSchemaClass:
    """ ExperimentTypeJsonSchema
    for handling generating the Json schema to validate each specific ExperimentType
        N.B. Currently many of the sets are not being done as they are slices of the core_dict
    """

    def __init__(self, experiment_type_obj: object, core_dict):
        self._experimentType = experiment_type_obj
        self.experiment_type_name = experiment_type_obj.experiment_type_name
        self._core_dict = core_dict
        self._specific_json_config = ""
        # below was uncommented in working! But was failing
        # self.set_experiment_specific_dict(experiment_type_obj.get_checklist_specific_dict())
        self.platform_instrument = ""
        self.SRA_obj = ""
        self._schema_dict = {}
        self.set_platform_instrument()
        experiment_type_obj.set_json_schema_obj(self)

    def get_experiment_type_obj(self):
        return self._experimentType

    def get_experiment_type_name(self):
        experimentType = self._experimentType
        return experimentType.experiment_type_name

    @property
    def get_SRA_obj(self):
        if hasattr(self, 'SRA_obj') and self.SRA_obj != '':
            self.SRA_obj
        else:
            # ic.disable()
            self.SRA_obj = get_SRA_XML_baseline()
            # ic.enable()
        return self.SRA_obj

    def set_platform_instrument(self):
        """
         gets the platform and instrument JSON configuration ultimately from the experiment_sra_xml
         e.g. {'BGISEQ': ['BGISEQ-500', 'MGISEQ-2000RS', 'BGISEQ-50'],
                'DNBSEQ': ['DNBSEQ-G50','DNBSEQ-G400 FAST','DNBSEQ-T7', 'unspecified','DNBSEQ-G400']
              }
        :return:
        """
        sra_xml_obj = self.get_SRA_obj
        # ic(sra_xml_obj)
        # self.platform_instrument = sra_xml_obj.get_platform()
        # schema_core_dict = {"properties": self.get_core_fields_dict()}
        # properties instrument_platform enum LIST
        # ic(self._core_dict['coreFields'])
        self._core_dict['coreFields']["instrument_platform"]["enum"] = sra_xml_obj.get_platform_list()
        # properties instrument_model enum LIST
        self._core_dict['coreFields']["instrument_model"]["enum"] = sra_xml_obj.get_instrument_list()
        self._core_dict['coreFields']["library_source"]["enum"] = sra_xml_obj.get_library_source_list()
        self._core_dict['coreFields']["library_selection"]["enum"] = sra_xml_obj.get_library_selection_list()
        self._core_dict['coreFields']["library_strategy"]["enum"] = sra_xml_obj.get_library_strategy_list()
        # target_loci

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
        required_terms = []
        excluding_terms = []
        for term in self.get_core_fields_dict_keylist():
            if "_comment" in term:
                excluding_terms.append(term)
            else:
                required_terms.append(term)
        # if len(excluding_terms) > 0:
        #     print(f"\tFYI: exclude: {excluding_terms} in {self.experiment_type_name}")
        # ic(required_terms)
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
                print(f"exclude: {term}")
            else:
                required_terms.append(term)
        # ic.enable()
        experiment_type_obj = self.get_experiment_type_obj()
        special_dict = experiment_type_obj.get_special_dict()
        # ic(special_dict)
        for term in list(special_dict.keys()):
            # ic(term)
            if "_comment" in term:
                print(f"exclude: {term}")
            else:
                required_terms.append(term)
        # ic(required_terms)

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

        # ic(self._core_dict['coreRules'])

        for platform in pi:
            # ic(platform)
            instrument = pi[platform]
            pi_rule = {'if': {'properties': {'instrument_platform': {'const': platform}}},
                       'then': {'properties': {'instrument': {'enum': instrument}}}}
            # ic(pi_rule)
            pi_rules.append(pi_rule)
            count += 1
        # ic(pi_rules)
        self._core_dict['coreRules'].extend(pi_rules)
        # ic(self._core_dict['coreRules'])
        # print(self._core_dict['coreRules'])

    def get_instrument_platform_rules(self):
        pass

    def get_core_rules_list(self):
        """get_core_fields_dict

        """
        # ic(self._core_dict['coreRules'])

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
        sra_xml_obj = self.get_SRA_obj
        # ic(experiment_specific_dict)
        all_specific_dict = self.get_all_specific_fields_json_config()
        my_specific_json_config = {}
        missing_atts = []
        for field in experiment_specific_dict:
            if field in all_specific_dict:
                my_specific_json_config[field] = all_specific_dict[field]
                my_specific_json_config[field]["default"] = experiment_specific_dict[field]
                my_specific_json_config[field]["_example"] = my_specific_json_config[field]["default"]
            else:
                missing_atts.append(field)
            # ic(my_specific_json_config)
        # if missing_atts:
        #     print(f"\tWARNING: need to add json config for {missing_atts} in {self.experiment_type_name}")

        # filling in some enums from the SRA_experiment object
        if my_specific_json_config.get('target_loci'):
            # ic()
            # ic(my_specific_json_config.get('target_loci'))
            # ic(sra_xml_obj.get_targetted_loci_list())
            my_specific_json_config['target_loci']['enum'] = sra_xml_obj.get_targeted_loci_list()
            # exit()
        self._specific_json_config = my_specific_json_config

    def get_experiment_specific_dict(self):
        """get_experiment_specific_dict
          getting the experiment type specific JSON configuration ( i.e. not the core fields )
          effectively many of the fields are core, but the assigned values are not, hence handling this way.

           N.B. this from the overall schema perspective for ALL experiments.
        What you will need to do is select just those fields in the checklist_specific, and overwrite the examples.

        """
        return self._specific_json_config

    def get_json_schema(self):
        """ get_json_schema
        generate a JSON_schema as a python schema specific to an experiment type
        This will ultimately be printed out as a json schema to validate the experiment_type
        return schema_dict
        """
        pass

        # ic("get_json_schema")

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
            # ic("already has _schema_dict")
            pass
        else:
            # ic("=" * 80)
            # ic("need to create a schema")
            schema_core_dict = {"properties": self.get_core_fields_dict()}
            # properties instrument_platform enum LIST
            # properties instrument_model enum LIST
            schema_rules_dict = {"allOf": self.get_core_rules_list()}
            # experiment_type_specific_dict = {"allOf": [self.get_experiment_specific_dict()]}
            # experiment_specific_dict = self.get_experiment_specific_dict()
            experiment_type_specific_dict = {"allOf": dict2objects(self.get_experiment_specific_dict())}
            # ic(experiment_type_specific_dict)
            # cl_metadata_dict["checklists"] = self.get_schema_metadata()
            """N.B. this does a deep merge of the dictionaries, most other methods did not..."""

            self._schema_dict = merge(schema_core_dict, self.get_schema_metadata(),
                                      experiment_type_specific_dict)
            # ic(schema_rules_dict)
            # ic(schema_rules_dict['allOf'])
            # rules = schema_rules_dict['allOf'].pop(0)    # tried, but it would not merge
            for rule in schema_rules_dict['allOf']:
                # ic(rule)
                self._schema_dict['allOf'].append(rule)
            self._schema_dict['allOf'].append({"required": self.get_allof_required_term_list()})
            self._schema_dict["required"] = self.get_properties_required_term_list()
            # ic(self._schema_dict['allOf'])
            # print("get the array of")
            # ic(schema_dict)
            # **json_schema_dict}
            return self._schema_dict

            def list2required(term_list):
                """

                :param term_list:
                :return: term_list[] =
                """
                tmp = {"required": term_list}
                return tmp

            schema_dict["allOf"].append(list2required(self.get_allof_required_term_list()))
            schema_dict["required"] = self.get_properties_required_term_list()
            self._schema_dict = schema_dict
            # ic(schema_dict)
        # ic(self._schema_dict)

        return self._schema_dict

    def print_json_schema(self):
        """ printout_json_schema to a JSON file
        params:
        return: json too

        """
        # ic()
        data_loc_dict = get_data_locations()
        json_schema_dict = self.get_json_schema()
        # ic(json_schema_dict)
        outfileName = data_loc_dict["schema_dir"] + self.experiment_type_name + '_schema.json'
        # ic(outfileName)

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
        # ic(my_dict['checklist_name'])
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
        if 'experiment_type_definition' in my_dict:
            return my_dict['experiment_type_definition'].replace("\n", " ")
        else:
            print("WARNING: No experiment_type_definition")
            return ""

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
        get_library_strategy will only return if field defined!!! Which will ofter not be true, so returns "" in
        those cases :return: term
        """
        # print("inside schema get_library_strategy")
        experiment_type_obj = self.get_experiment_type_obj()
        my_dict = experiment_type_obj.get_all_dict()
        # stwing = json.dumps(my_dict, indent=4)
        # print(f"my_dict={stwing}")
        # print(my_dict['library_strategy'])
        # ic(my_dict['library_strategy'])
        return my_dict.get('library_strategy', "")

    def get_library_selection(self):
        """

        :return: term
        """
        experiment_type_obj = self.get_experiment_type_obj()
        my_dict = experiment_type_obj.get_all_dict()
        # ic(my_dict['library_selection'])
        return my_dict['library_selection']
