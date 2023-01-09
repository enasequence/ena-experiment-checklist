# a single comment
"""Script to computationally generates the experimental checklist JSON files for users to enter data into.
It is driven by a single JSON config file.

___author___ = "woollard@ebi.ac.uk"
___start_date___ = "2022-11-29"
__docformat___ = 'reStructuredText'

"""
#python3 -m pydoc -w ExperimentChecklists2Json

from icecream import ic
import subprocess
import sys
import getopt
import requests
from requests.structures import CaseInsensitiveDict

import os
from os.path import join, dirname
import json
from jsonschema import validate
import pandas as pd


def printChecklist(checklistDict):
    """
    params:
        in: the JSON/dict to print
    """
    data_loc_dict = get_data_locations()

    ic(checklistDict)
    outfileName = data_loc_dict["output_dir"] + checklistDict['experiment_type'] + '.json'
    ic(outfileName)

    json_object = json.dumps(checklistDict, indent=4, sort_keys=True
    
    
    )
    ic(outfileName)
    with open(outfileName, "w") as outfile:
        outfile.write(json_object)

def getCoreDict(config_data):
    """
    extract the core fields as JSON entries
    params:
        in: the full config_json
        rtn: coreDict elements of the config_json
    """
    ic(config_data['coreFields'])
    coreDict={}
    for i in config_data['coreFields']:
        print(i)
        if isinstance(config_data['coreFields'][i], dict):
                coreDict[i] = ""
                #ic(type(config_data['coreFields'][i]))
                #ic("dict: " + str(config_data['coreFields'][i]))
        else:
            # ic("!dict:" + str(config_data['coreFields'][i]))
            coreDict[i] = config_data['coreFields'][i]
    ic(coreDict)
    #quit()
    return(coreDict)

def addSpecials(mergedChecklistDict,config_data):
    """ method to check for and pull out the json for special field cases in 
        each checklist, from the config_data file.
    params:
        in: mergedChecklistDict,config_data
        rtn: mergedChecklistDict
    """
    ic()
    
    jsonKey = 'pcr_fields'
    if jsonKey in mergedChecklistDict:
        ic("yipeee key exists:" + jsonKey)
        ic(config_data[jsonKey])
        mergedChecklistDict = {**mergedChecklistDict, **config_data[jsonKey]}
        del mergedChecklistDict[jsonKey]
        ic(mergedChecklistDict)


    return(mergedChecklistDict)


def getFields(config_data):
    """ method to get all the fields needed for a particular checklist and to instruct the printing
        of the combined fields JSON to a file 
        in: config_data
        rtn: mergedChecklistDict
    """
    coreDict = getCoreDict(config_data)
    ic(coreDict)
    ic(config_data['experimentTypes'])
    for etype in config_data['experimentTypes']:
        print(etype)
        checklistDict = {}
        for field in etype.keys():
            #ic(config_data[etype][field]['enum'])
            ic(field, etype[field])
            checklistDict[field] = etype[field]
        mergedChecklistDict = {**checklistDict, **coreDict} 
        mergedChecklistDict = addSpecials(mergedChecklistDict,config_data)
        printChecklist(mergedChecklistDict)
        
def get_data_locations():
    """ get_data_locations
    params:
        rtn: data_loc_dict
    """
    data_loc_dict = {}
    data_loc_dict["base_dir"] ="/Users/woollard/projects/easi-genomics/ExperimentChecklist/"
    data_loc_dict["input_dir"] = data_loc_dict["base_dir"] + "data/input/"
    data_loc_dict["output_dir"] = data_loc_dict["base_dir"] + "data/output/"

    return data_loc_dict

def readConfig():
    """ readConfig
    params:
        rtn: JSON
    """

    data_loc_dict = get_data_locations()
    filename = data_loc_dict["input_dir"] + "ExperimentChecklistIn.json"
    ic(filename)
    f = open(filename)
    data = json.load(f)
    f.close()
    return(data)


def main():
    ic("'afternoon")
    config_data = readConfig()
    getFields(config_data)







if __name__ == '__main__':
    main()
