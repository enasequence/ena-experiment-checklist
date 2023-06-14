#!/usr/bin/env python3
"""Script of 'validate.py' is to validate json template files against a schema'

validate_file(test_file, schema_file) is all you need external

___author___ = "woollard@ebi.ac.uk"
___start_date___ = 2023-04-11
__docformat___ = 'reStructuredText'

"""
import sys

from icecream import ic
import json
#import JsonSchema
from jsonschema import validate
import os
import subprocess
import re

def JSONFILE2string(json_file_name):
    """

    :param json_file_name:
    :return:
    """
    with open(json_file_name, "r") as myfile:
        jsonData = json.load(myfile)
    return(jsonData)

def clean_validation(output):
        """
        Function to clean the biovalidation output.
        Puts it into md style
        :param output:
        :return:
        """
        output.replace(":\\n \\n", ":").replace("\\n,", "<-------").replace("\\t", "").replace("b' ", "")
        output.replace("\\n \\nValidation finished.", "").replace("\\n", " ").replace("/", "\n/").replace("\\'", "'")
        #   print("FAILED---->" +output)
        output = re.sub('^.*Validation failed with errors:', 'Validation failed with errors', output)
        # the next 3 lines clean up things I could not do
        output = output.replace("\\n", '__nl__')
        output = output.replace('__nl__', '\n')
        output = output.replace("\\t", ' ')
        output = output.replace("\n\n", "\n")

        # get the  one per line
        output = output.replace("\n\\.", "\n* ")
        output = output.replace("\n \\.", "\n* ")
        output = re.sub("\n\\.", "\n* ", output)
        output = re.sub("\n[ ]\.", "\n* ", output)
        output = output.replace("\n/", "\n* ")
        output = output.replace("\n \n", "\n")
        output = output.replace("\\\'", "\"")
        output = output.replace("\n should", ": should")
        output = output.replace("data should", "\n* data should")
        output = output.replace(", data", "\n* data")
        output = re.sub("[, ]*\n", "\n", output)
        output = output.replace("\n Validation", "\n\nValidation")

        # output = output.split("\n")
        output = re.sub("[\n\' ]*$", "", output)
        return output
        # sys.exit()
def validate_file(test_file, schema_file):
    ic()
    test_cmd = "node  /Users/woollard/projects/biovalidator/biovalidator/src/biovalidator.js  -d " \
                   +  test_file + " -s " + schema_file + "| sed -e 's/\x1b\[[0-9;]*m//g';s/^[\]*//g"

    ic(test_cmd)
    ic(f"{schema_file} {test_file}")
    temp = subprocess.run([test_cmd], shell = True, capture_output = True)
    output = str(temp.stdout)

    if "Validation passed successfully" in output:
            output="Validation passed successfully"
    else:
            output = clean_validation(output)

    return output
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

def validate_suite(schema_dir, test_file_dir, test_status):
    """

    :param basedir:
    :return:
    """

    testing_pairs = {}

    if test_status == True:
        testing_pairs["TEST_type_schema.json"] = ["TEST_type_works.json", "TEST_type_fails.json"]
        testing_pairs["METABARCODING_schema.json"] = ["METABARCODING_works.json", "METABARCODING_fails.json"]
        testing_pairs["METATRANSCRIPTOMIC_schema.json"] = ["METATRANSCRIPTOMIC_works.json","METATRANSCRIPTOMIC_fails.json"]
        testing_pairs["GENOMIC_schema.json"] = ["GENOMIC_works.json", "GENOMIC_fails.json"]
        testing_pairs["TRANSCRIPTOMIC_schema.json"] = ["TRANSCRIPTOMIC_works.json","TRANSCRIPTOMIC_fails.json"]
    else:
        ic(test_file_dir)
        for test_file in os.listdir(test_file_dir):
            ic(test_file)
            schema_file = test_file.replace(".json", "_schema.json")
            ic(schema_file)
            testing_pairs[schema_file] = [test_file]

    ic(testing_pairs)

    for schema_file in testing_pairs:
        for test_file in testing_pairs[schema_file]:
            # test_cmd = "node  /Users/woollard/projects/easi-genomics/biovalidator/validator-cli.js  validator-cli.js -j " \
            #        + test_file_dir + "/" + test_file + " -s " + schema_dir + "/" + schema_file + "| sed -e 's/\x1b\[[0-9;]*m//g';s/^[\]*//g"
            raw_output = output = validate_file(test_file_dir + test_file, schema_dir + schema_file)
            # print(output)
            if "Validation passed successfully" in output:
                ic("PASSED---->No validation errors reported")
            else:

                # ic(output)
                print(f"FAILED---->{test_file}  vs {schema_file}")
                print(output)
                print("________________________________________")

    # works
    # node /Users/woollard/projects/biovalidator/biovalidator/src/biovalidator.js  -d /Users/woollard/projects/easi-genomics/ExperimentChecklist/data/output_test/real_testing//TRANSCRIPTOMIC_fails.json -s /Users/woollard/projects/easi-genomics/ExperimentChecklist/data/schema//TRANSCRIPTOMIC_schema.json



def main():
    basedir = "/Users/woollard/projects/easi-genomics/ExperimentChecklist/"
    schema_file = basedir + "data/schema/TEST_type_schema2.json"
    schema_file = basedir + "data/schema/noddy1.json"
    validate_schema(basedir, schema_file)
    schema_dir = basedir + "data/schema/"
    test_file_dir = basedir + "data/output_test/real_testing/"
    #validate_suite(schema_dir, test_file_dir, True)
    test_file_dir = basedir + "data/output_test/filled_templates/"
    validate_suite(schema_dir, test_file_dir, False)

if __name__ == '__main__':
    ic()
    main()
