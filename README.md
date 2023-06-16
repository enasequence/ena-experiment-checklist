# ExperimentChecklist
The aim of this project is to generate JSON templates and JSON schemas for Experiment Checklists used for the ENA. 
Each experiment type will have a specific a pair of JSON checklist template and JSON schema. 
The data and code in this repository generate these.

During the users' workflow, the filled out checklist template will be validated against the relevant JSON schema.


![](docs/ExptChecklistpng.png)

## Background

Sample metadata has been explicitly captured with checklist templates for years. 

Experiment metadata collected to date however has been rather limited. With the increasing use of NGS and related technologies to study the general biological world, and human health care in particular, there is a broader spread of sequencing experiment related metadata that could usefully be collected. This metadata information will increase the usefulness and quality of the data, by making it more FAIR(Find-ability,Accessibility,Interoperable and Reusable).

The proposal to meet user needs is to have an experimental checklist similar to that implemented for the sample level checklists. A key difference here is to use the JSON schema and bio-validation technologies, to do the initial validation, catch most issues and provide rapid feedback to users. Deeper validation will still be needed and performed to ensure meeting of INSDC standards, although it is anticipated that few issues will be found. 

There is a core of essential metadata, with other metadata that is often experiment and sequencing technology specific, hence the need for a handful of checklists; it is currently unknown if the same schema can be used for all. 

User use cases have been collated and some key user and maintenance technical requirements have been developed. In parallel to the technical development, there will need to be work to determine the future needs and waves of experimental checklists.

## In Essence
* The "everything" JSON template is taken from data/input/ExperimentChecklistIn.json
* A script runs over this and generates specific JSON templates in data/output for each experiment type.
* The same script generates experiment type documentation too.

![](docs/ExperimentChecklistSimple.png)
## Further docs
* [For more technical details](docs/ExperimentChecklistTechnicalDoc.md)
* [Directory organisation overview](docs/directory_organisation_explanation.md)
* [Experiment Type Specific Info](docs/experiment_types/)