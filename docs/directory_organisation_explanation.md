# Directory Organisation 

## Background
There is a very simple directory structure.  
:minidisc: for :recycle: of experimental data to make it FAIR

## ./ directory
* readme.md - general background
* the subdirectories are listed below

## source directory
* ExperimentChecklists2Json.py - script that generates the **experiment checklist template** and 
* test_ExperimentChecklists2Json.py

## docs directory
* ExperimentChecklistTechnicalDoc.md - more technical background
* directory_organisation_explanation.md
* ExptChecklistpng.png


## data directory
### ./examples:

### ./data/input: - JSON file that specifies for all the experiments types what fields and values are needed.
This is what to **edit** if one wishes to make a change
* ExperimentChecklistIn.json
* test_ExperimentChecklistIn.json

### schema: - these are the schemas that the filled out template will be tested against.
* GENOMIC_schema.json
* METABARCODING_schema.json
* METATRANSCRIPTOMIC_schema.json
* TEST_schema.json
* TEST_schema_hack.json
* TEST_type_schema.json
* TRANSCRIPTOMIC_schema.json

### output: - - automatically generated template
* GENOMIC.json
* METABARCODING.json
* METATRANSCRIPTOMIC.json
* TEST.json
* TEST_hack.json
* TEST_type.json
* TRANSCRIPTOMIC.json

### output_test: - automatically generated template
* GENOMIC.json
* METABARCODING.json
* METATRANSCRIPTOMIC.json
* TEST.json
* TEST_type.json
* TRANSCRIPTOMIC.json
