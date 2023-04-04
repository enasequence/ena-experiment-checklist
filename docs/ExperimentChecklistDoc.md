# This is the Experiment Checklist Documentation</title>

N.B. this will probably go to READTHEDOCS

## Introduction
The Experiment Checklists are an effort to create template to capture 
better metadata about experiments. The Sample Checklists have shown us how to usefully 
capture metadata, but also how to do this better.

This will include details of what is mandatory and the allowable controlled vocabulary

JSON schema rather than XML is the chosen technology as it has many advantages.

![](ExptChecklistpng.png)

## Technology chosen was JSON schema
There are many advantages of JSON Schema over the older, but still venerable XML..
* JSON schema is more readily human readable than XML. Both are machine readable.
* Validation is very easy for things like controlled vobularies.
* Dependency programming is relatively easy in JSON schema.

## Overview of How We Intend this to Work

* Programmatically manage the different Experiment Checklists
* Have each of the end product JSON checklists versioned.
* Have each of the end product JSON checklists validate. that can be immediately 
validated by user.

This generates JSON templates and JSON schemas for Experiment Checklists used for the ENA. There is a pair of JSON checklist template and JSON schema for each experiment type.
The aim is that we get higher quality metadata and due the versioning we can just 
add improved JSON 