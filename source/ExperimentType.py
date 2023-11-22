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

