# This is the Experiment Checklist more Technically Focused Documentation

N.B. this will probably go to READTHEDOCS

<!-- TOC -->
* [This is the Experiment Checklist more Technically Focused Documentation](#this-is-the-experiment-checklist-more-technically-focused-documentation)
  * [Introduction](#introduction)
  * [Key Features](#key-features)
  * [Technology chosen was JSON schema](#technology-chosen-was-json-schema)
  * [Overview of How We Intend this to Work](#overview-of-how-we-intend-this-to-work)
  * [Valdation examples](#valdation-examples)
    * [internal testing](#internal-testing)
    * [User Testing](#user-testing)
<!-- TOC -->

## Introduction

The Experiment Checklists are an effort to create template to capture
better metadata about experiments. The Sample Checklists have shown us how to usefully
capture metadata, but also how to do this better.

[see README.md](../README.md) for more information about the purpose of this.
[for user aspects](ExperimentChecklistUserDoc.md)

## Key Features

* a pair of JSON schema and JSON template per experiment type. The filled out template is validated against the schema.
* details of what fields mandatory
* conditional mandatory aspects allowed, e.g. if PCR then PCR values need to be provided.
* allowable controlled vocabulary
* JSON schema rather than XML is the chosen technology as it has many advantages.

![ExperimentChecklistGraphically](ExperimentChecklistGraphically.png)

## Technology chosen was JSON schema

There are many advantages of JSON Schema over the older, but still venerable XML..

* JSON schema is more readily human-readable than XML. Both are machine-readable.
* Validation is very easy for things like controlled vocabularies.
* Dependency programming is relatively easy in JSON schema.

## Overview of How We Intend this to Work

* Programmatically manage the different Experiment Checklists
* Have each of the end product JSON checklists versioned.
* Have each of the end product JSON checklists validate. that can be immediately
validated by user.

This generates JSON templates and JSON schemas for Experiment Checklists used for the ENA. There is a pair of JSON checklist template and JSON schema for each experiment type.
The aim is that we get higher quality metadata and due to the versioning we can just
add improved JSON to future versions as needed, without worrying about backwards compatibility.

## Valdation examples

### internal testing

For this is it is necessary to:

* Have biovalidator installed and setup.
* The current output of the validation (BTW: TEST_type is set-up to have most terms encountered across the all the experiments)

```python
ic| testing_pairs: {'GENOMIC_schema.json': ['GENOMIC_works.json', 'GENOMIC_fails.json'],
                    'METABARCODING_schema.json': ['METABARCODING_works.json',
                                                  'METABARCODING_fails.json'],
                    'METATRANSCRIPTOMIC_schema.json': ['METATRANSCRIPTOMIC_works.json',
                                                       'METATRANSCRIPTOMIC_fails.json'],
                    'TEST_type_schema.json': ['TEST_type_works.json', 'TEST_type_fails.json'],
                    'TRANSCRIPTOMIC_schema.json': ['TRANSCRIPTOMIC_works.json',
                                                   'TRANSCRIPTOMIC_fails.json']}
ic| f"{schema_file} {test_file}": 'TEST_type_schema.json TEST_type_works.json'
ic| 'No validation errors reported'
ic| f"{schema_file} {test_file}": 'TEST_type_schema.json TEST_type_fails.json'
The validation process has found the following error(s): .pcr_primers should have required property \'pcr_primers\'  should match "then" schema 
/instrument_platform should be equal to one of the allowed values: ["BGISEQ","CAPILLARY","DNBSEQ","ILLUMINA","ION_TORRENT","LS454","OXFORD_NANOPORE","PACBIO_SMRT"] 
/sample_accession should match pattern "(^SAM(E|D|N)[A-Z]?[0-9]+)|(^(E|D|S)RS[0-9]{6,})" 
/study_id should match pattern "(^(E|D|S)RP[0-9]{6,})|(^PRJ(E|D|N)[A-Z][0-9]+)" '
ic| f"{schema_file} {test_file}": 'METABARCODING_schema.json METABARCODING_works.json'
ic| 'No validation errors reported'
ic| f"{schema_file} {test_file}": 'METABARCODING_schema.json METABARCODING_fails.json'
b" The validation process has found the following error(s): .target_loci should have required property 'target_loci' "
ic| f"{schema_file} {test_file}": 'METATRANSCRIPTOMIC_schema.json METATRANSCRIPTOMIC_works.json'
ic| 'No validation errors reported'
ic| f"{schema_file} {test_file}": 'METATRANSCRIPTOMIC_schema.json METATRANSCRIPTOMIC_fails.json'
The validation process has found the following error(s): 
/library_strategy should be equal to one of the allowed values: ["AMPLICON","ATAC-seq","Bisulfite-Seq","CLONE","CLONEEND","CTS","ChIA-PET","ChIP-Seq","DNase-Hypersensitivity","EST","FAIRE-seq","FINISHING","FL-cDNA","Hi-C","MBD-Seq","MNase-Seq","MRE-Seq","MeDIP-Seq","OTHER","POOLCLONE","RAD-Seq","RIP-Seq","RNA-Seq","SELEX","Synthetic-Long-Read","Targeted-Capture","Tethered Chromatin Conformation Capture","Tn-Seq","VALIDATION","WCS","WGA","WGS","WXS","miRNA-Seq","ssRNA-seq"] '
ic| f"{schema_file} {test_file}": 'GENOMIC_schema.json GENOMIC_works.json'
ic| 'No validation errors reported'
ic| f"{schema_file} {test_file}": 'GENOMIC_schema.json GENOMIC_fails.json'
The validation process has found the following error(s): 
/instrument_model should be equal to one of the allowed values: ["454 GS 20","454 GS FLX Titanium","454 GS FLX","454 GS FLX+","454 GS Junior","454 GS","AB 310 Genetic Analyzer","AB 3130 Genetic Analyzer","AB 3130xL Genetic Analyzer","AB 3500 Genetic Analyzer","AB 3500xL Genetic Analyzer","AB 3730 Genetic Analyzer","AB 3730xL Genetic Analyzer","BGISEQ-500","DNBSEQ-G400 FAST","DNBSEQ-G400","DNBSEQ-G50","DNBSEQ-T7","GridION","HiSeq X Five","HiSeq X Ten","Illumina Genome Analyzer II","Illumina Genome Analyzer IIx","Illumina Genome Analyzer","Illumina HiScanSQ","Illumina HiSeq 1000","Illumina HiSeq 1500","Illumina HiSeq 2000","Illumina HiSeq 2500","Illumina HiSeq 3000","Illumina HiSeq 4000","Illumina MiSeq","Illumina MiniSeq","Illumina NovaSeq 6000","Illumina iSeq 100","Ion Torrent PGM","Ion Torrent Proton","Ion Torrent S5 XL","Ion Torrent S5","MinION","NextSeq 500","NextSeq 550","PacBio RS II","PacBio RS","PromethION","Sequel","unspecified"] '
ic| f"{schema_file} {test_file}": 'TRANSCRIPTOMIC_schema.json TRANSCRIPTOMIC_works.json'
ic| 'No validation errors reported'
ic| f"{schema_file} {test_file}": 'TRANSCRIPTOMIC_schema.json TRANSCRIPTOMIC_fails.json'
The validation process has found the following error(s): 
/instrument_platform should be equal to one of the allowed values: ["BGISEQ","CAPILLARY","DNBSEQ","ILLUMINA","ION_TORRENT","LS454","OXFORD_NANOPORE","PACBIO_SMRT"] 
/library_strategy should be equal to one of the allowed values: ["AMPLICON","ATAC-seq","Bisulfite-Seq","CLONE","CLONEEND","CTS","ChIA-PET","ChIP-Seq","DNase-Hypersensitivity","EST","FAIRE-seq","FINISHING","FL-cDNA","Hi-C","MBD-Seq","MNase-Seq","MRE-Seq","MeDIP-Seq","OTHER","POOLCLONE","RAD-Seq","RIP-Seq","RNA-Seq","SELEX","Synthetic-Long-Read","Targeted-Capture","Tethered Chromatin Conformation Capture","Tn-Seq","VALIDATION","WCS","WGA","WGS","WXS","miRNA-Seq","ssRNA-seq"] 
/sample_accession should match pattern "(^SAM(E|D|N)[A-Z]?[0-9]+)|(^(E|D|S)RS[0-9]{6,})" 
/study_id should match pattern "(^(E|D|S)RP[0-9]{6,})|(^PRJ(E|D|N)[A-Z][0-9]+)" '
```

### User Testing

* users will need to validate every ***experiment*** JSON file against the relevant schema
* We may need to get set up a web service to simplify this.

***
![ExptChecklistpng](ExptChecklistpng.png)
