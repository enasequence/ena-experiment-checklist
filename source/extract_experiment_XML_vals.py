#!/usr/bin/env python3
"""Script of 'extractXMLvals.py' is to '

___author___ = "woollard@ebi.ac.uk"
___start_date___ = 2023-05-03
__docformat___ = 'reStructuredText'

"""


from icecream import ic

import argparse
import subprocess
import os
import json

class SRA_SPEC:
    def __init__(self, my_sra_json):
        self.schema_level = my_sra_json["xs:schema"]
        #ic(self.schema_level)
        self.process_platform()

    def process_platform(self):
        simple_level = self.schema_level["xs:simpleType"]
        ic(simple_level)
        ic("_____________________________")
        self.platform = {}
        all_instruments = []
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

        platforms = self.get_platform_list()
        all_instruments = list(set(all_instruments)) # get rid of duplicates
        self.all_instruments = all_instruments

    def get_platform(self):
        return(self.platform)

    def get_platform_list(self):
        return(list(self.platform.keys()))

    def get_instrument_list(self):
        return (self.all_instruments)


    def print_platform_md_list(self):
        platforms = self.get_platform_list()
        platforms.sort()
        for platform in platforms:
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
    # cmd = ('date', '-u', '+%A')
    #
    # p = subprocess.run(cmd, capture_output = True, text = True)
    # print(p.stdout)
    outdir = "/Users/woollard/projects/easi-genomics/ExperimentChecklist/data/input/"
    outfile = "SRA.common.json"
    outfullfilename=outdir + outfile
    cmd="curl https://ftp.ebi.ac.uk/pub/databases/ena/doc/xsd/sra_1_5/SRA.common.xsd | xq > " + outfullfilename
    ic(cmd)
    #os.system(cmd)

    f = open(outfullfilename)
    my_sra_json=json.load(f)
    #ic(my_sra_json)
    sra_instance = SRA_SPEC(my_sra_json)
    #ic(sra_instance.get_platform())
    return(sra_instance)

def main():
    sra_obj = get_SRA_XML_baseline()
    ic(sra_obj.get_platform())
    print("platform terms")
    sra_obj.print_platform_md_list()
    print("instrument terms")
    sra_obj.print_instrument_md_list()

if __name__ == '__main__':
    ic()
    main()
