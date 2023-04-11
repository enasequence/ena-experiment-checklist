#!/usr/bin/env python3
"""Script of 'validate.py' is to '

___author___ = "woollard@ebi.ac.uk"
___start_date___ = 2023-04-11
__docformat___ = 'reStructuredText'

"""


from icecream import ic
import json
#import JsonSchema
from jsonschema import validate

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

def main():
    basedir = "/Users/woollard/projects/easi-genomics/ExperimentChecklist/"
    schema_file = basedir + "data/schema/TEST_type_schema2.json"
    schema_file = basedir + "data/schema/noddy1.json"
    validate_schema(basedir, schema_file)

if __name__ == '__main__':
    ic()
    main()
