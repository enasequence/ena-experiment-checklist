#!/usr/bin/env python3
"""SRA_EXPERIMENT_OBJ.py is a simple object and methods for SRA_EXPERIMENT
   it also contains the get_SRA_XML_baseline object. This provides much of the raw data
   needed for the SRA_EXPERIMENT object and indeed calls this.

___author___ = "woollard@ebi.ac.uk"
___start_date___ = 2024-01-31
__docformat___ = 'reStructuredText'

"""

import datetime
import json
import os
import os.path
import sys
from datetime import datetime
from datetime import timedelta
from datetime import timezone

from icecream import ic
from openpyxl.workbook import child


class SRA_EXPERIMENT_SPEC:
    def __init__(self, my_sra_experiment_json, my_sra_common_json):
        self.common_schema_level = my_sra_common_json["xs:schema"]
        self.experiment_schema_level = my_sra_experiment_json["xs:schema"]
        self.targeted_loci_dict = {}
        self.process_experiment()
        #ic(self.schema_level)
        self.process_platform()

    def process_experiment(self):
        ic.disable()
        ic()
        simple_level = self.experiment_schema_level["xs:simpleType"]
        #ic(simple_level)
        ic("_____________________________")

        def process_lib_child(child, self_child_pointer):
            ic.disable()
            # print("inside process_lib_child")
            ic()
            ic(self_child_pointer)
            #ic(child['xs:annotation']['xs:documentation'])
            #ic(child['xs:restriction']['xs:enumeration'])
            for LibChild in child['xs:restriction']['xs:enumeration']:
                term_name = LibChild['@value']
                ic(term_name)
                if LibChild.get('xs:annotation'):
                    ic(LibChild['xs:annotation']['xs:documentation'])
                    self_child_pointer[term_name] = {}
                    self_child_pointer[term_name]["documentation"] = LibChild['xs:annotation'][
                        'xs:documentation'].replace("\n", " ").replace("  ", " ").replace("  ", " ").removesuffix(" ")
                else:
                    self_child_pointer[term_name] = {}
                    self_child_pointer[term_name]["documentation"] = ""
            #print(f"-->{self_child_pointer}")
        for child in simple_level:
            # ic()
            if child.get('@name'):
                field = child['@name'].removeprefix("type")
            else:
                field = child['xs:restriction'].removeprefix("type")
            #ic(field)
            #print(f"------>{field}<-----")
            if field == "LibraryStrategy":
                self.library_strategy = {}
                process_lib_child(child, self.library_strategy)
            elif field == "LibrarySource":
                self.library_source = {}
                process_lib_child(child, self.library_source)
            elif field == "LibrarySelection":
                self.library_selection = {}
                process_lib_child(child, self.library_selection)
            else:
                ic(f"WARNING<--TBD--> {field}")


        self.process_further_expt()
        #ic(self.get_targetted_loci_list())
        # ic()
        ic.enable()

    def process_targeted_loci(self, element):
        """
        process_targeted_loci is quite complex.
        :param element:
        :return: nowt, but do add a dictionary to self.targeted_loci_dict

        """
        ic()

        locus_name_struct=element["xs:complexType"]["xs:sequence"]["xs:element"]["xs:complexType"]["xs:attribute"][0]
        # print(locus_name_struct["xs:simpleType"])
        locus_name_enum=locus_name_struct["xs:simpleType"]["xs:restriction"]["xs:enumeration"]

        targeted_loci_dict = { "locus_name": {}}
        for value in locus_name_enum:
            # ic(value)
            targeted_loci_dict['locus_name'][value['@value']] = value['xs:annotation']['xs:documentation']
        self.targeted_loci_dict = targeted_loci_dict



    def process_further_expt(self):
        ic.disable()

        def process_complex(pointer):
            ic()
            for child in pointer:
             #ic(child.keys())
             if "@name" in child:
                 ic(child["@name"])
                 if child["@name"] == "LibraryDescriptorType":
                     ic()
                     ic(child['xs:sequence'].keys())
                     base = child['xs:sequence']['xs:element']
                     for element in base:
                         if element['@name'] == 'TARGETED_LOCI':
                             ic(element)
                             ic(element['@name'])
                             self.process_targeted_loci(element)
                     ic()

        complex_level = self.experiment_schema_level["xs:complexType"]
        process_complex(complex_level)

        ic.enable()

    def get_library_strategy_details(self):
        # e.g. 'ChIA-PET': {'documentation': 'Direct sequencing of proximity-ligated chromatin immunoprecipitates.'},
        return self.library_strategy

    def get_library_strategy_detail(self, lib_strat):
        # print("inside get_library_strategy_detail")
        # print(f"term={lib_strat}")
        if lib_strat == "":
            return ""
        else:
            ic(lib_strat)
            lib_strat_dict = self.library_strategy
            my_val = lib_strat_dict.get(lib_strat, "ERROR")
            # print(f"my lib_strat_dict val={my_val}")

            if (my_val == "ERROR"):
                print(f"ERROR: an invalid library_strategy term is being used: {lib_strat}", file=sys.stderr)
            else:
                ic(self.library_strategy[lib_strat])
                return self.library_strategy[lib_strat]['documentation']

    def get_library_selection_details(self):
        # e.g. 'ChIA-PET': {'documentation': 'Direct sequencing of proximity-ligated chromatin immunoprecipitates.'},
        return self.library_selection

    def get_library_selection_detail(self, term):
        if term == "":
            return ""
        else:
            ic(term)
            ic(self.library_selection[term])
            return self.library_selection[term]['documentation']

    def get_library_source_details(self):
        # e.g. 'ChIA-PET': {'documentation': 'Direct sequencing of proximity-ligated chromatin immunoprecipitates.'},
        return self.library_source

    def get_library_source_detail(self, term):
        if term == "":
            return ""
        else:
            ic(term)
            ic(self.library_source[term])
            return self.library_source[term]['documentation']

    def get_library_strategy_list(self):
        my_list = list(self.library_strategy.keys())
        my_list.sort
        return my_list

    def get_library_source_list(self):
        my_list = list(self.library_source.keys())
        my_list.sort
        return my_list

    def get_library_selection_list(self):
        my_list = list(self.library_selection.keys())
        my_list.sort
        return my_list

    def process_platform(self):
        simple_level = self.common_schema_level["xs:simpleType"]
        #ic(simple_level)
        #ic("_____________________________")
        self.platform = {}
        all_instruments = []
        # if frequent changes may be best to refactor and pull the platform names directly from the XML and dynamically re-map.
        # it looked convoluted in the XML and JSON to do, so went for the easiest option.
        missing_platforms = []
        for child in simple_level:
            raw_platform = child['@name'].removeprefix("type").removesuffix("Model")
            if raw_platform == "Illumina":
                platform = "ILLUMINA"
            elif raw_platform == "Iontorrent":
                platform = "ION_TORRENT"
            elif raw_platform == "454":
                platform = "LS454"
            elif raw_platform == "PacBio":
                platform = "PACBIO_SMRT"
            elif raw_platform == "Capillary":
                platform = "CAPILLARY"
            elif raw_platform == "OxfordNanopore":
                platform = "OXFORD_NANOPORE"
            elif raw_platform == "BGISEQ":
                platform = "BGISEQ"
            elif raw_platform == "DnbSeq":
                platform = "DNBSEQ"
            elif raw_platform == "Ultima":
                platform = "ULTIMA"
            elif raw_platform == "Element":
                platform = "ELEMENT"
            elif raw_platform == "CG":
                platform = "COMPLETE_GENOMICS"
            elif raw_platform == "AbiSolid":
                platform = "ABI_SOLID"
            elif raw_platform == "Helicos":
                platform = "HELICOS"
            elif raw_platform == "VelaDiagnostics":
                platform = "VELA_DIAGNOSTICS"
            elif raw_platform == "Genapsys":
                platform = "GENAPSYS"
            elif raw_platform == "GeneMind":
                platform = "GENE_MIND"
            elif raw_platform == "Tapestri":
                platform = "TAPESTRI"
            else:
                platform = "not_yet_recognised"
                # Ultima , Element, Helicos, Complete Genomics, AbiSolid
                missing_platforms.append(raw_platform)

            values = child['xs:restriction']['xs:enumeration']
            instruments = []
            #ic(self.platform)
            if not self.platform.get(platform):
                self.platform[platform] = instruments
            for value_child in values:
                instrument = value_child['@value']
                instruments.append(instrument)
            self.platform[platform].extend(instruments)
            self.platform[platform] = list(set(self.platform[platform]))   # get rid of duplicates
            all_instruments.extend(instruments)

        if len(missing_platforms) > 0:
            os.write(2, b"WARNING: the following platforms are not recognised yet, please add in to process_platform() before continuing!\n")
            print(f"Missing platforms: \"{missing_platforms}\"")
            exit()

        platforms = self.get_platform_list()
        # ic(self.get_platform_list())
        all_instruments = list(set(all_instruments)) # get rid of duplicates
        all_instruments.sort()
        self.all_instruments = all_instruments
        # ic(self.get_instrument_list())

    def get_platform(self):
        return(self.platform)

    def get_instrument(self):
        return(self.all_instruments)

    def get_platform_list(self):
        """
        :return: platform_list - alphabetically sorted
        """
        platforms = list(self.platform.keys())
        platforms.sort()
        return platforms

    def get_platform_and_instruments(self):
        """
        :return:  the current platform and instrument as JSON object
        """
        return self.platform

    def get_instrument_list(self):
        """
        :return: instrument_list - alphabetically sorted
        """
        return list(self.all_instruments)

    def get_targeted_loci_dict(self):
        """
        targeted_loci_dict['locus_name'][value['@value']] = value['xs:annotation']['xs:documentation']

        :return:
        """
        return self.targeted_loci_dict
    def get_targeted_loci_list(self):
        """

        :return:
        """
        # ic(list(self.targeted_loci_dict['locus_name'].keys()))
        return sorted(self.targeted_loci_dict['locus_name'].keys())

    def print_platform_md_list(self):
        platforms = self.get_platform_list()
        for platform in platforms:
            if platform == "not_yet_recognised":
                os.write(2, b"WARNING: the following platform is not recognised yet, please add in!\n")
                print(f"MISSING platform: \"{platform}\"")
            print("- " + platform)

    def print_instrument_md_list(self):
        all_instruments = self.get_instrument_list()
        all_instruments.sort()
        for instrument in all_instruments:
            print("- " + instrument)
    """=====================END OF SRA OBJ=============================="""

def get_SRA_XML_baseline():
    """
    updates the local copies of INSDC XML XSD and returns an object
    :return: sra_object_instance
    """
    # ic("_____inside get_SRA_XML_baseline_____")

    def file2json(file_name):
        f = open(file_name)
        my_sra_json = json.load(f)
        f.close()
        return(my_sra_json)

    def cmd2file(cmd, outfilename):
        """

        :param cmd:
        :param outfilename:
        :return:
        """
        ic()
        ic(cmd)
        ic(outfilename)
        pid = os.getpid()
        tmp_outfile = "/tmp/tmp_exp_checklist_" + str(pid)
        tmp_cmd = cmd + " > " + tmp_outfile
        ic(tmp_cmd)
        try:
            os.system(tmp_cmd)
        except:
            print(f"ERROR: command failed: {tmp_cmd}")
            sys.exit()

        try:
            os.rename(tmp_outfile, outfilename)
        except:
            print(f"ERROR: command failed: 'os.rename(tmp_outfile, outfilename)'")
            sys.exit()

    def is_file_older_than(file_name, delta):
        """
        e.g. is_file_older_than(file_name, timedelta(days=1))
        :param file_name:
        :param delta:
        :return: True or False
        """
        if not os.path.exists(file_name):
            return False
        # cutoff = datetime.utcnow() - delta
        cutoff = datetime.now(tz=timezone.utc) - delta
        # ic(f"cutoff={cutoff}")
        mtime = datetime.fromtimestamp(os.path.getmtime(file_name), tz=timezone.utc)
        # ic(f"mtime={mtime}")
        if mtime < cutoff:
            return True
        return False

    def cmd2json(cmd, outfilename):
        """


        :param cmd:  command without a stdout to a file e.g. curl https://ftp.ebi.ac.uk/pub/databases/ena/doc/xsd/sra_1_5/SRA.experiment.xsd | xq
        :param outfilename:
        :return: my_sra_json
        """
        # ic()
        #ic(cmd)
        # ic(outfilename)

        if not os.path.isfile(outfilename) or is_file_older_than(outfilename, timedelta(days=1)):
            print(f"{outfilename} is older than 1 day! so re-running.")
            cmd2file(cmd, outfilename)

        my_sra_json = file2json(outfilename)

        #sys.exit()
        return my_sra_json

    # Check and do any necessary updates
    # Sorry will run on linux and unix files, and needs jq installed
    HOMEDIR = os.environ.get("HOME")
    outdir = HOMEDIR + "/projects/ExperimentChecklist/data/input/"
    # ic(outdir)
    outfile = "SRA.common.json"
    outfullfilename = outdir + outfile
    cmd = "curl https://ftp.ebi.ac.uk/pub/databases/ena/doc/xsd/sra_1_5/SRA.common.xsd | xq "

    my_sra_common_json = cmd2json(cmd, outfullfilename)

    outfile = "SRA.experiment.json"
    outfullfilename = outdir + outfile
    cmd = "curl https://ftp.ebi.ac.uk/pub/databases/ena/doc/xsd/sra_1_5/SRA.experiment.xsd | xq "
    my_sra_experiment_json = cmd2json(cmd, outfullfilename)

    sra_obj = SRA_EXPERIMENT_SPEC(my_sra_experiment_json, my_sra_common_json)
    return(sra_obj)

