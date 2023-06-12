#!/usr/bin/env python3
"""Script of 'validate.py' is to validate json template files against a schema'

___author___ = "woollard@ebi.ac.uk"
___start_date___ = 2023-04-11
__docformat___ = 'reStructuredText'

"""


from icecream import ic
import json
#import JsonSchema
from jsonschema import validate
# import os
import subprocess

def JSONFILE2string(json_file_name):
    """

    :param json_file_name:
    :return:
    """
    with open(json_file_name, "r") as myfile:
        jsonData = json.load(myfile)
    return(jsonData)
def validate_schema(basedir, schema_file):
    """

    :param schema_file:
    :return:
    """
    ic()
    ic(f"{schema_file}")
    json_schema_string = JSONFILE2string(schema_file)
    if(len(json_schema_string) >= 1):
        ic(json_schema_string, ' is valid JSON')
    ic(len(json_schema_string))
    test_json_file = basedir + "data/output_test/TEST_type.json"
    test_json_file = basedir + "data/output_test/TEST_type_noddy1.json"
    test_json = JSONFILE2string(test_json_file)
    ic(test_json)
    validation_result = validate(instance=test_json, schema=json_schema_string)
    ic(validation_result)

def validate_suite(basedir):
    """

    :param basedir:
    :return:
    """
    schema_dir = basedir + "data/schema/"
    test_file_dir = basedir + "data/output_test/real_testing/"
    testing_pairs = {}
    testing_pairs["TEST_type_schema.json"] = []
    testing_pairs["TEST_type_schema.json"].append("TEST_type_works.json")
    testing_pairs["TEST_type_schema.json"].append("TEST_type_fails.json")
    testing_pairs["METABARCODING_schema.json"] = []
    testing_pairs["METABARCODING_schema.json"].append("METABARCODING_works.json")
    testing_pairs["METABARCODING_schema.json"].append("METABARCODING_fails.json")
    testing_pairs["METATRANSCRIPTOMIC_schema.json"] = []
    testing_pairs["METATRANSCRIPTOMIC_schema.json"].append("METATRANSCRIPTOMIC_works.json")
    testing_pairs["METATRANSCRIPTOMIC_schema.json"].append("METATRANSCRIPTOMIC_fails.json")
    testing_pairs["GENOMIC_schema.json"] = []
    testing_pairs["GENOMIC_schema.json"].append("GENOMIC_works.json")
    testing_pairs["GENOMIC_schema.json"].append("GENOMIC_fails.json")
    testing_pairs["TRANSCRIPTOMIC_schema.json"] = []
    testing_pairs["TRANSCRIPTOMIC_schema.json"].append("TRANSCRIPTOMIC_works.json")
    testing_pairs["TRANSCRIPTOMIC_schema.json"].append("TRANSCRIPTOMIC_fails.json")

    ic(testing_pairs)
    # works
    # node /Users/woollard/projects/biovalidator/biovalidator/src/biovalidator.js  -d /Users/woollard/projects/easi-genomics/ExperimentChecklist/data/output_test/real_testing//TRANSCRIPTOMIC_fails.json -s /Users/woollard/projects/easi-genomics/ExperimentChecklist/data/schema//TRANSCRIPTOMIC_schema.json

    for schema_file in testing_pairs:
        for test_file in testing_pairs[schema_file]:
            # test_cmd = "node  /Users/woollard/projects/easi-genomics/biovalidator/validator-cli.js  validator-cli.js -j " \
            #        + test_file_dir + "/" + test_file + " -s " + schema_dir + "/" + schema_file + "| sed -e 's/\x1b\[[0-9;]*m//g';s/^[\]*//g"
            test_cmd = "node  /Users/woollard/projects/biovalidator/biovalidator/src/biovalidator.js  -d " \
                       + test_file_dir + "/" + test_file + " -s " + schema_dir + "/" + schema_file + "| sed -e 's/\x1b\[[0-9;]*m//g';s/^[\]*//g"

            ic(test_cmd)
            ic(f"{schema_file} {test_file}")
            temp = subprocess.run([test_cmd], shell=True, capture_output=True)
            output = str(temp.stdout)
            if "No validation errors reported" in output:
                ic("No validation errors reported")
            else:
                output = output.replace(":\\n \\n", ":").replace("\\n,", "<-------").replace("\\t", "").replace("b' ", "")
                output = output.replace("\\n \\nValidation finished.", "").replace("\\n", " ").replace("/", "\n/")
                #ic(output)
                print(output)
        sys.exit()
def main():
    basedir = "/Users/woollard/projects/easi-genomics/ExperimentChecklist/"
    schema_file = basedir + "data/schema/TEST_type_schema2.json"
    schema_file = basedir + "data/schema/noddy1.json"
    validate_schema(basedir, schema_file)

    validate_suite(basedir)

if __name__ == '__main__':
    ic()
    main()
