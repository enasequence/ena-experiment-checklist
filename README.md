# ExperimentChecklist
This generates JSON templates and JSON schemas for Experiment Checklists used for the ENA. 
There is a pair of JSON checklist template and JSON schema for each experiment type.

The data and code in this repo.  generate these.

![](docs/ExptChecklistpng.png)

## Background

Sample metadata has been explicitly captured with checklist templates for a number of years.

Experiment metadata collected to date however has been rather limited. With the increasing use of NGS and related technologies to study the general biological world, and human health care in particular, there is a broader spread of sequencing experiment related metadata that could usefully be collected. This metadata information will increase the usefulness and quality of the data, by making it more FAIR(Find-ability,Accessibility,Interoperable and Reusable).

The proposal to meet user needs is to have an experimental checklist similar to that implemented for the sample level checklists. A key difference here is to use the JSON schema and bio-validation technologies, to do the initial validation, catch most issues and provide rapid feedback to users. Deeper validation will still be needed. 

There is a core of essential metadata, with other metadata that is often experiment and sequencing technology specific, hence the need for a handful of checklists; it is currently unknown if the same schema can be used for all. 

User use cases have been collated and some key user and maintenance technical requirements have been developed. In parallel to the technical development, there will need to be work to determine the first wave of experimental checklists.

## In Essence
* The "everything" JSON template is taken from data/input/ExperimentChecklistIn.json
* A script runs over this and generates specific JSON templates in data/output for each experiment type


[For more details)[docs/ExperimentChecklistDoc.md]