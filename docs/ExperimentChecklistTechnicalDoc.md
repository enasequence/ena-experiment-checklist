# This is the Experiment Checklist more Technically Focused Documentation


N.B. this will probably go to READTHEDOCS

## Introduction
The Experiment Checklists are an effort to create template to capture 
better metadata about experiments. The Sample Checklists have shown us how to usefully 
capture metadata, but also how to do this better.

[see README.md](../README.md) for more information about the purpose of this.

## Key Features
* a pair of JSON schema and JSON template per experiment type. The filled out template is validated against the schema. 
* details of what fields mandatory 
* conditional mandatory aspects allowed, e.g. if PCR then PCR values need to be provided.
* allowable controlled vocabulary


JSON schema rather than XML is the chosen technology as it has many advantages.

![](ExptChecklistpng.png)

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

![](ExperimentChecklistSimple.png)