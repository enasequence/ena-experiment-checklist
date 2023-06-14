#!/usr/bin/env python3
"""Script of 'validate_preparation.py' is to prepare files for validation testing'

___author___ = "woollard@ebi.ac.uk"
___start_date___ = 2023-06-14
__docformat___ = 'reStructuredText'
chmod a+x validate_preparation.py
"""
import sys

from icecream import ic
import os
from os.path import join, dirname

import argparse
import json
from validate import validate_file

def file2json(filename):
    ic(filename)
    f = open(filename, "r")
    json_obj = json.load(f)
    f.close()
    # ic(json_obj)
    return json_obj

def dict2file(my_dict, outfilename):
    ic(outfilename)
    json_object = json.dumps(my_dict, indent = 4, sort_keys = True)
    with open(outfilename, "w") as outfile:
        outfile.write(json_object)

def get_prefilled_dict():
    key_field_dict = {
    'experiment_name': "my experiment_name",
    'study_id': "ERP123456",
    'sample_accession': "SAME123456",
    "instrument_platform": "ILLUMINA",
    "instrument_model": "HiSeq X Ten",
    "library_layout": "PAIRED",
    "library_selection": "unspecified",
    "iibrary_strategy": "WGS"
    }

    return key_field_dict

def fill(template_dir, filled_dir, schema_dir):
    """"""
    ic()
    for template in os.listdir(template_dir):
        ic(template)
        template_full_name = template_dir + template
        json_obj = file2json(template_full_name)
        schema_full_name = schema_dir + template.replace(".json", "_schema.json")
        prefilled_dict = get_prefilled_dict()
        for field in prefilled_dict:
            if field in json_obj and json_obj[field] == "":
                json_obj[field] = prefilled_dict[field]
        filled_out_template_file = filled_dir + template
        dict2file(json_obj, filled_out_template_file)
        output = validate_file(filled_out_template_file, schema_full_name)
        print(output)


def main():
    basedir = "/Users/woollard/projects/easi-genomics/ExperimentChecklist/"
    filled_dir = basedir + "data/output_test/filled_templates/"
    template_dir = basedir + "data/output/"
    schema_dir = basedir + "data/schema/"
    fill(template_dir, filled_dir, schema_dir)

if __name__ == '__main__':
    ic()
    main()
