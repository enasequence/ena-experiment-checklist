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
import subprocess
import os
import json
import os.path
import time
import datetime
from datetime import timedelta
from datetime import timezone
from datetime import datetime

from SRA_EXPERIMENT_OBJ import SRA_EXPERIMENT_SPEC



def get_SRA_XML_baseline():
    """
    Does more than just provided the XML.
    IT returns an object.

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
        pid = os.getpid()
        tmp_outfile = "/tmp/tmp_exp_checklist_" + str(pid)
        tmp_cmd = cmd + " > " + tmp_outfile
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

    outdir = "/Users/woollard/projects/easi-genomics/ExperimentChecklist/data/input/"
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

    sra_obj.get_platform_and_instruments()
    print("End of Main")

if __name__ == '__main__':
    ic()
    main()
