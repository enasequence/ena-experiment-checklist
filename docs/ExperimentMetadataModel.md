# Experiment Metadata Models
<!-- TOC -->
* [Experiment Metadata Models](#experiment-metadata-models)
  * [Context](#context)
  * [Experiment MetaModel](#experiment-metamodel)
  * [Experiment Metadata](#experiment-metadata)
<!-- TOC -->

## Context of the Models
The ENA metadata model: 

https://ena-docs.readthedocs.io/en/latest/submit/general-guide/metadata.html

![ENA metadata model](https://ena-docs.readthedocs.io/en/latest/_images/metadata_model_whole.png)

## The Sequencing Experiment MetaModel

```mermaid
stateDiagram
      Attribute-->Term
      Term-->Value
      Value-->ControlledTextValues
      Value-->ControlledDataType
      Value-->FreeText
      ExperimentType --> Core
      ExperimentType --> ExperimentSpecific
      Core --> Attribute: cadence and requirement status
      ExperimentSpecific --> Attribute: cadence and requirement status


```


## The Sequencing Experiment Metadata