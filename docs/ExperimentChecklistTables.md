# experiments type checklists
## Introduction
These are the checklists for different types of experiments.
## References: metadata model and glossary
 * https://ena-docs.readthedocs.io/en/latest/submit/general-guide/metadata.html
 * https://ena-docs.readthedocs.io/en/latest/submit/reads/webin-cli.html - includes most controlled vocabularly terms
N.B. the Experiment Type Name is typically a combination of the overall approach and the molecular type(library_source) under investigation

## Table of most important fields in each experiment template
| Checklist Group | Checklist Name | Checklist ID | Checklist Description | Checklist Version | Experiment Type Name | Experiment Type Definition | Experiment Design | Library Strategy | Library Source | Library_Selection |
| --- | --- | --- | --- | --- | --- | --- | --- |--- | --- | -- |
| METAGENOMIC | METABARCODING specific | EXC000001 | Experiment Metadata Checklist Focused on metabarcoding | v1 | METABARCODING | Metabarcoding is the barcoding of DNA/RNA (or eDNA/eRNA) in a manner that allows for the simultaneous identification of many taxa within the same sample. The main difference between barcoding and metabarcoding is that metabarcoding does not focus on one specific organism, but instead aims to determine species composition within a sample.[WIKIPEDIA] | mixed marker barcoding | AMPLICON | METAGENOMIC | PCR | 
| METAGENOMIC | METAGENOMIC sequencing specific | EXC000002 | Experiment Metadata Checklist Focused on metagenomics | v1 | METAGENOMIC_SEQUENCING | Approach which samples, in parallel, all genes in all organisms present in a given sample, e.g. to provide insight into biodiversity and function. |  |  | METAGENOMIC |  | 
| METAGENOMIC | METATRANSCRIPTOMIC specific | EXC000003 | Experiment Metadata Checklist Focused on metatranscriptomics | v1 | METATRANSCRIPTOMIC | The study of microbe gene expression within natural environments (i.e. the metatranscriptome). Metatranscriptomics methods can be used for whole gene expression profiling of complex microbial communities.[EDAM] |  |  | METATRANSCRIPTOMIC |  | 
| GENOMIC | GENOMIC specific | EXC000010 | Experiment Metadata Checklist Focused on genomics | v1 | GENOMIC | Sequencing of DNA located in the genome and able to be transmitted to the offspring.[adapted from SO] |  |  | GENOMIC |  | 
| GENOMIC | Viral RNA specific | EXC000012 | Experiment Metadata Checklist Focused on Viral RNA | v1 | VIRAL_RNA_GENOME | Adapted from a virus whose genome consists of RNA. Can be single or double-stranded RNA.[NCIT and SO adapted] |  |  | VIRAL_RNA |  | 
| GENOMIC | Exome sequencing specific | EXC000013 | Experiment Metadata Checklist Focused on exome sequencing | v1 | EXOME_SEQUENCING | Laboratory technique to sequence all the protein-coding regions in a genome, i.e., the exome. Exome sequencing is considered a cheap alternative to whole genome sequencing. |  |  | GENOMIC |  | 
| TEST_group | TEST_name | EXC999999 | Experiment Metadata Checklist Focused on TEST | v1 | TEST_type | TEST DEFINITION |  |  | TRANSCRIPTOMIC |  | 
| TRANSCRIPTOMIC | TRANSCRIPTOMIC specific | EXC000020 | Experiment Metadata Checklist Focused on transcriptomics | v1 | TRANSCRIPTOMIC | The analysis of transcriptomes, or a set of all the RNA molecules in a specific cell, tissue etc. |  |  | TRANSCRIPTOMIC |  | 
| TRANSCRIPTOMIC | SPATIAL TRANSCRIPTOMIC specific | EXC000021 | Experiment Metadata Checklist Focused on SPATIAL TRANSCRIPTOMIC | v1 | SPATIAL_TRANSCRIPTOMIC | assay that allows visualization and quantitative analysis of the transcriptome with spatial resolution in individual tissue sections |  |  | TRANSCRIPTOMIC |  | 
| GENOTYPING | BARCODING specific | EXC000030 | Experiment Metadata Checklist Focused on barcoding | v1 | DNA_BARCODING | Analyse DNA sequences in order to identify a DNA 'barcode'; marker genes or any short fragment(s) of DNA that are useful to diagnose the taxa of biological organisms. | single target locus and single species barcoding | AMPLICON | GENOMIC | PCR | 
| GENOTYPING | GENOTYPING specific | EXC000031 | Experiment Metadata Checklist Focused on genotyping | v1 | GENOTYPING | An assay in which variation in a part of or the whole genome is analysed |  |  | GENOMIC |  | 
| BEYOND_DNA | CHROMOSOME CONFORMATION CAPTURE specific | EXC000040 | Experiment Metadata Checklist Focused on chromosome conformation capture | v1 | CHROMOSOME_CONFORMATION_CAPTURE |  |  |  | GENOMIC??? |  | 
| BEYOND_DNA | EPIGENOMICS specific | EXC000041 | Experiment Metadata Checklist Focused on epigenomics | v1 | EPIGENOMICS | The study of the epigenetic modifications of a whole cell, tissue, organism etc. Epigenetics concerns the heritable changes in gene expression owing to mechanisms other than DNA sequence variation. |  |  | GENOMIC??? |  | 
| BEYOND_DNA | Chromatin specific | EXC000042 | Experiment Metadata Checklist Focused on Chromatin, nucleosome and DNA binding site prediction | v1 | CHROMATIN_RELATED |  | dd |  | GENOMIC??? |  | 
