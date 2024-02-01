#!/usr/bin/env python3
"""Script of 'extract_experiment_XML_vals.py' is to get various experiment related controlled vocabularies and dependencies from the SRA.experiment.xml

1) the underlying functions are called  in the ExperimentChecklists2.json.py script
2) as a command line - If someone needs to repeat getting an alphabetically sorted list of terms for 1) platforms and 2) instruments run this script.

Notes:
It pulls the information from the SRA.experiment.xsd. This XSD is the ground truth for metadata for experiments, thus important
to be in sync with it. The code automatically uses the latest version on the ftp site.
(BTW I cheat and use a JSON rendition of the XML, as JSON is much easier to use in python.
Uses the fairly ubiquitous jq/xq utilities. Only needed though when the XML is updated.)

___author___ = "woollard@ebi.ac.uk"
___start_date___ = 2023-05-03
__docformat___ = 'reStructuredText'

"""
import sys

from icecream import ic

import argparse

import pprint
from SRA_EXPERIMENT_OBJ import SRA_EXPERIMENT_SPEC, get_SRA_XML_baseline





def list2string(my_list):
    """
    :param my_list:
    :return: string that is for a alphabetically sorted list and newline delimited
    """
    my_list.sort()
    return '\n'.join(my_list)

def main():
    ic.enable()
    sra_obj = get_SRA_XML_baseline()

    # ic(sra_obj.get_platform())
    # ic(sra_obj.get_platform_list())
    # ic(sra_obj.get_instrument_list())
    loc_count = 0
    ic(sra_obj.get_library_strategy_list())
    ic(sra_obj.get_library_strategy_list())
    print(list2string(sra_obj.get_library_strategy_list()))
    print(f"++++ {loc_count} ++++")
    loc_count += 1
    ic(sra_obj.get_library_source_list())
    print(list2string(sra_obj.get_library_source_list()))
    print(f"++++ {loc_count} ++++")
    loc_count += 1
    ic(sra_obj.get_library_source_list())
    print(list2string(sra_obj.get_library_selection_list()))
    print(f"++++ {loc_count} ++++")
    loc_count += 1

    print("platform terms")
    sra_obj.print_platform_md_list()
    print("\ninstrument terms")
    sra_obj.print_instrument_md_list()

    print("\nplatform_and_instruments")
    pprint.PrettyPrinter(width=100).pprint(sra_obj.get_platform_and_instruments())

    print("\ntargeted_locus_names:")
    print(sra_obj.get_targeted_loci_list())
    print("End of Main\n####################################################")

if __name__ == '__main__':
    ic()
    main()
