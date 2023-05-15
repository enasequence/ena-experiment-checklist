#!/usr/bin/env python3
"""Script of 'extract_experiment_XML_vals.py' is to get various experiment related controlled vocabularies and dependencies from the SRA.experiment.xml

1) the underlying functions are called  in the ExperimentChecklists2.json.py script
2) as a command line - If someone needs to repeat getting an alphabetically sorted list of terms for 1) platforms and 2) instruments run this script.

Notes:
It pulls the information from the SRA.experiment.xml. This XML is the ground truth for metadata for experiments, thus important
to be in sync with it.
(BTW I cheat and use a JSON rendition of the XML, as JSON is much easier to use in python.
Uses the fairly ubiquitous jq/xq utilities. Only needed though when the XML is updated.)

___author___ = "woollard@ebi.ac.uk"
___start_date___ = 2023-05-03
__docformat___ = 'reStructuredText'

"""


from icecream import ic

import argparse
import subprocess
import os
import json

class SRA_EXPERIMENT_SPEC:
    def __init__(self, my_sra_experiment_json, my_sra_common_json):
        self.common_schema_level = my_sra_common_json["xs:schema"]
        self.experiment_schema_level = my_sra_experiment_json["xs:schema"]
        self.process_experiment()
        #ic(self.schema_level)
        self.process_platform()

    def process_experiment(self):
        ic()
        simple_level = self.experiment_schema_level["xs:simpleType"]
        #ic(simple_level)
        ic("_____________________________")

        def process_lib_child(child, self_child_pointer):
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
                        'xs:documentation']

        for child in simple_level:
            ic()
            if child.get('@name'):
                field = child['@name'].removeprefix("type")
            else:
                field = child['xs:restriction'].removeprefix("type")
            ic(field)
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
                ic("<--TBD-->")


        self.process_further_expt()
        ic(self.get_targetted_loci_list())
        ic()

    def process_further_expt(self):
        ic()
        complex_level = self.experiment_schema_level["xs:complexType"]
        #ic(complex_level)

        def process_complex(pointer):
            ic()
            #ic(pointer)

            base = child['xs:complexContent']['xs:extension']
            # ic(base)
            # ic(base['@base'].removeprefix("com"))
            el_base = base['xs:choice']['xs:element']
            #ic(el_base)
            ic(el_base['@name'])
            ic(el_base['xs:annotation']['xs:documentation'])
            #ic(el_base['xs:complexType']['xs:sequence']['xs:element'])
            elements_base = el_base['xs:complexType']['xs:sequence']['xs:element']
            for member in elements_base:
                ic(member['@name'])
                if member['@name'] == 'MEMBER':
                    ic(member['xs:annotation']['xs:documentation'])
                elif member['@name'] == 'DEFAULT_MEMBER':
                    ic(member['xs:annotation']['xs:documentation'])

        self.locus = {}

        for child in complex_level:
            ic()
            #ic(child)
            if child.get('@name'):
                field = child['@name'].removeprefix("type")
                ic(field)
                if field == 'SampleDescriptorType':
                    #ic(child)
                    self.SampleDescriptor = {}
                    process_complex(self.SampleDescriptor)
                elif field == 'LibraryDescriptorType':
                    ic()
                    #ic(child)
                    el_base = child['xs:sequence']['xs:element']
                    for grandchild in el_base:
                        #ic(grandchild)
                        if grandchild['@name'] == 'TARGETED_LOCI':
                            loci_base = grandchild['xs:complexType']['xs:sequence']['xs:element']['xs:complexType']['xs:attribute']
                            #ic(loci_base)
                            for locus in loci_base:
                                #ic(locus)

                                if locus.get('xs:simpleType'):
                                    locus_base = locus['xs:simpleType']['xs:restriction']['xs:enumeration']
                                    for locus_val in locus_base:
                                        #ic(locus_val)
                                        value = locus_val['@value']
                                        #ic(value)
                                        self.locus[value] = {}
                                        self.locus[value] = locus_val['xs:annotation']['xs:documentation']
                                        #ic(self.locus)
                            ic(self.locus)



                elif field == 'PoolMemberType':
                    ic()
                    self.PoolMemberType = {}
                    base = child['xs:complexContent']['xs:extension']
                    #ic(base)
                    #ic(base['@base'].removeprefix("com"))
                    for grandchild in base['xs:attribute']:
                        name = grandchild['@name']
                        ic(grandchild['@name'])
                        # ic(grandchild['@type'].removeprefix('xs:'))
                        # ic(grandchild['xs:annotation']['xs:documentation'])
                        self.PoolMemberType[name] = {}
                        self.PoolMemberType[name]['type'] = grandchild['@type'].removeprefix('xs:')
                        self.PoolMemberType[name]['docs'] = grandchild['xs:annotation']['xs:documentation']
                        self.PoolMemberType[name]['value'] = ""
                        for tag in base['xs:sequence']['xs:element']:
                            #ic(tag)

                            if tag == '@name':
                                tag_base = base['xs:sequence']['xs:element'][tag]
                                tag_deep_base = base['xs:sequence']['xs:element']['xs:complexType']['xs:simpleContent']['xs:extension']['xs:attribute']
                                self.PoolMemberType[name]['sequence'] = {}
                                self.PoolMemberType[name]['sequence'][tag_deep_base['@name']] = {}
                                self.PoolMemberType[name]['sequence'][tag_deep_base['@name']]['type'] = tag_deep_base['@type'].removeprefix('xs:')
                                self.PoolMemberType[name]['sequence'][tag_deep_base['@name']]['value'] = ""
                                self.PoolMemberType[name]['sequence']['docs'] = tag_deep_base['xs:annotation']['xs:documentation']
                    ic(self.PoolMemberType)
            else:
                ic()

        ic()


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
        ic()
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
            os.write(2, b"WARNING: the following platforms are not recognised yet, please add in before continuing!\n")
            print(f"Missing platforms: \"{missing_platforms}\"")
            exit()

        platforms = self.get_platform_list()
        # ic(self.get_platform_list())
        all_instruments = list(set(all_instruments)) # get rid of duplicates
        all_instruments.sort()
        self.all_instruments = all_instruments
        # ic(self.get_instrument_list())
        ic()

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

    def get_instrument_list(self):
        """
        :return: instrument_list - alphabetically sorted
        """
        return list(self.all_instruments)

    def get_targetted_loci_dict(self):
        return self.locus
    def get_targetted_loci_list(self):
        targetted_loci = list(self.get_targetted_loci_dict().keys())
        targetted_loci.sort()
        return targetted_loci

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

    :return: sra_instance
    """
    ic()

    def cmd2json(cmd):
        ic(cmd)
        # os.system(cmd)
        f = open(outfullfilename)
        my_sra_json = json.load(f)
        f.close()
        return my_sra_json

    outdir = "/Users/woollard/projects/easi-genomics/ExperimentChecklist/data/input/"
    outfile = "SRA.common.json"
    outfullfilename = outdir + outfile
    cmd = "curl https://ftp.ebi.ac.uk/pub/databases/ena/doc/xsd/sra_1_5/SRA.common.xsd | xq > " + outfullfilename
    outfile = "SRA.experiment.json"
    my_sra_common_json = cmd2json(cmd)

    outfullfilename = outdir + outfile
    cmd = "curl https://ftp.ebi.ac.uk/pub/databases/ena/doc/xsd/sra_1_5/SRA.experiment.xsd | xq > " + outfullfilename
    my_sra_experiment_json = cmd2json(cmd)

    sra_obj = SRA_EXPERIMENT_SPEC(my_sra_experiment_json, my_sra_common_json)
    return(sra_obj)


def main():
    sra_obj = get_SRA_XML_baseline()

    # ic(sra_obj.get_platform())
    # ic(sra_obj.get_platform_list())
    # ic(sra_obj.get_instrument_list())

    ic(sra_obj.get_library_strategy_list())
    ic(sra_obj.get_library_source_list())
    ic(sra_obj.get_library_selection_list())

    exit()


    # print("platform terms")
    # sra_obj.print_platform_md_list()
    # print("\ninstrument terms")
    # sra_obj.print_instrument_md_list()

    ic(sra_obj.get_targetted_loci_list())
    ic()

if __name__ == '__main__':
    ic()
    main()
