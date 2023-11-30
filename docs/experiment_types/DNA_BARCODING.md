# DNA_BARCODING

**Description:** Experiment Metadata Checklist Focused on barcoding

## Introduction

The purpose of this template is to collect high quality sequencing experiment related metadata.This is an automatically generated document designed to help the populating of the JSON template for the above experiment type.
The first table is specific to the experiment type, with the second core to all. Some of the fields are:

* mandatory and some optional
* have controlled terms or specific patterns
* others are free text

Some of the controlled terms may not be applicable for your particular experiment_type, they are there for completeness.

## Please Note

* This template **allows 1 or more experiments' metadata** to be submitted. If >1 experiments: in JSON style, please add a comma at the end of the previous record just after the closing }.
* **This is just guidance in one place to help you populate the template.** N.B. It may become out of date or plain wrong. So please refer to official INSDC docs in case of conflict.

## DNA_BARCODING Experiment Specific Fields

| Field name | Definition | Mandatory | Example | Type | Controlled Vocab Terms | Comment |
| --- | --- | --- | --- | --- | --- | --- |
| checklist_id | checklist identifier | True | EXC000030 | string |  |  |
| checklist_name | A short descriptive name to human identify | False | BARCODING specific | string |  |  |
| checklist_version | The version of this checklist, allows us to validate the write records against the right checklist version | True | v1 | integer |  | Version of the format v[[::digit::]] e..g. v2 |
| checklist_group | The collection of the experiment checklists | False | BARCODING | string |  |  |
| experiment_type | The broad type of sequencing experiment performed. A mixture of library strategy and source | True | DNA_BARCODING | string |  |  |
| target_loci | Names the gene(s) or locus(loci) or other genomic feature(s) targeted by the sequence.[INSDC adapted] | False |  | string | 16S rRNA, 18S rRNA, 28S rRNA, COX1, ITS1-5.8S-ITS2, RBCL, exome, matK, other |  |
| target_subfragment |  | False |  | string |  |  |
| design_description | The library design including library properties, layout, protocol, targeting information, and spot and gap descriptors. | True | single target locus and single species barcoding | string |  |  |
| _comment | These are all possible fields not in the core, with their JSON configs | False |  | string |  |  |
| design_description | The library design including library properties, layout, protocol, targeting information, and spot and gap descriptors. | True |  | string |  |  |
| checklist_id | checklist identifier | True |  | string |  |  |
| checklist_name | A short descriptive name to human identify | False |  | string |  |  |
| checklist_version | The version of this checklist, allows us to validate the write records against the right checklist version | True |  | integer |  | Version of the format v[[::digit::]] e..g. v2 |
| checklist_group | The collection of the experiment checklists | False |  | string |  |  |
| experiment_type | The broad type of sequencing experiment performed. A mixture of library strategy and source | True |  | string |  |  |
| target_loci | Names the gene(s) or locus(loci) or other genomic feature(s) targeted by the sequence.[INSDC adapted] | False |  | string | 16S rRNA, 18S rRNA, 28S rRNA, COX1, ITS1-5.8S-ITS2, RBCL, exome, matK, other |  |
| target_subfragment |  | False |  | string |  |  |
| pcr_protocol | PCR is a method for amplifying a DNA base sequence using multiple rounds of heat denaturation of the DNA and annealing of oligonucleotide primers complementary to flanking regions in the presence of a heat-stable polymerase. This results in duplication of the targeted DNA region. Newly synthesized DNA strands can subsequently serve as additional templates for the same primer sequences, so that successive rounds of primer annealing, strand elongation, and dissociation produce rapid and highly specific amplification of the desired sequence. PCR also can be used to detect the existence of the defined sequence in a DNA sample.[NCIT] A PCR protocol is the precise recipe followed for the type of PCR,. | False |  | string |  | see the pcr_primers fields too |
| pcr_primers | PCR primers that were used to amplify the sequence of the targeted gene, locus or subfragment. This field should contain all the primers used for a single PCR reaction if multiple forward or reverse primers are present in a single PCR reaction. The primer sequence should be reported in uppercase letters.[INSDC] | False |  | string |  |  |
| multiplex_identifiers | The barcoding identifiers used to label DNA fragments during muliplex sequencing | False |  | string |  |  |
| adapters | Adapters provide priming sequences for both amplification and sequencing of the sample-library fragments. Both adapters should be reported; in uppercase letters.[INSDC] | False |  | string |  |  |
| sequence_related | sequence format type, filename and checksum[INSDC] | True |  | string |  | This section allows one to provide sequence file names. The sequences can be in fastq, CRAM and BAM. N.B. BAM filers do not needs to be assemblies and BAM is slightly favoured over fastq as it is more compressed. |

## Core Fields

| Field name | Definition | Mandatory | Example | Controlled Vocab Terms | Comment |
| --- | --- | --- | --- | --- | --- |
| study_id | This is the study accession number that starts with ERP granted after registering a study with the ENA. [ENA] | True | ERP1234567 | (^(E\|D\|S)RP[0-9]{6,})\|(^PRJ(E\|D\|N)[A-Z][0-9]+) |  |
| sample_accession | This is the study accession number that starts with ERP granted after registering a study with the ENA. [ENA] | True |  | (^SAM(E\|D\|N)[A-Z]?[0-9]+)\|(^(E\|D\|S)RS[0-9]{6,}) |  |
| library_layout | Reads are unpaired (usual case).[ENA] | False | SINGLE | SINGLE, PAIRED |  |
| experiment_name | A unique name of the experiment within your study. An experiment is the sequencing activity that generates one or more sequencing runs on a specific sample. [ENA] | False | my lovely TRANSCRIPTOMICS experiment |  |  |
| library_source | The LIBRARY_SOURCE specifies the type of source material that is being sequenced. [INSDC] | True | TRANSCRIPTOMIC | GENOMIC, GENOMIC SINGLE CELL, TRANSCRIPTOMIC, TRANSCRIPTOMIC SINGLE CELL, METAGENOMIC, METATRANSCRIPTOMIC, SYNTHETIC, VIRAL RNA, OTHER |  |
| library_strategy | Sequencing technique intended for this library.[INSDC] | True | RNA-Seq | WGS, WGA, WXS, RNA-Seq, ssRNA-seq, snRNA-seq, miRNA-Seq, ncRNA-Seq, FL-cDNA, EST, Hi-C, ATAC-seq, WCS, RAD-Seq, CLONE, POOLCLONE, AMPLICON, CLONEEND, FINISHING, ChIP-Seq, MNase-Seq, DNase-Hypersensitivity, Bisulfite-Seq, CTS, MRE-Seq, MeDIP-Seq, MBD-Seq, Tn-Seq, VALIDATION, FAIRE-seq, SELEX, RIP-Seq, ChIA-PET, Synthetic-Long-Read, Targeted-Capture, Tethered Chromatin Conformation Capture, NOMe-Seq, ChM-Seq, GBS, Ribo-Seq, OTHER |  |
| library_selection | Method used to enrich the target in the sequence library preparation. [INSDC] | True | unspecified | RANDOM, PCR, RANDOM PCR, RT-PCR, HMPR, MF, repeat fractionation, size fractionation, MSLL, cDNA, cDNA_randomPriming, cDNA_oligo_dT, PolyA, Oligo-dT, Inverse rRNA, Inverse rRNA selection, ChIP, ChIP-Seq, MNase, DNase, Hybrid Selection, Reduced Representation, Restriction Digest, 5-methylcytidine antibody, MBD2 protein methyl-CpG binding domain, CAGE, RACE, MDA, padlock probes capture method, other, unspecified |  |
| library_name | The name of the nucleotide sequencing library. [NCIT] | False |  |  |  |
| library_description | The free description of the nucleotide sequencing library. [NCIT adapted] | False |  |  |  |
| insert_size | The average insert size found during nucleic acid sequencing. [NCIT] | False | 0 |  |  |
| instrument_platform | The name of the technology platform used to perform nucleic acid sequencing. [NCIT] | True | ILLUMINA | ABI_SOLID, BGISEQ, CAPILLARY, COMPLETE_GENOMICS, DNBSEQ, ELEMENT, HELICOS, ILLUMINA, ION_TORRENT, LS454, OXFORD_NANOPORE, PACBIO_SMRT, ULTIMA |  will get values from the sra.experiment_xml |
| instrument_model | The name and/or number associated with a specific sequencing instrument model.  [NCIT-adapted] | False | unspecified | 454 GS, 454 GS 20, 454 GS FLX, 454 GS FLX Titanium, 454 GS FLX+, 454 GS Junior, AB 310 Genetic Analyzer, AB 3130 Genetic Analyzer, AB 3130xL Genetic Analyzer, AB 3500 Genetic Analyzer, AB 3500xL Genetic Analyzer, AB 3730 Genetic Analyzer, AB 3730xL Genetic Analyzer, AB 5500 Genetic Analyzer, AB 5500xl Genetic Analyzer, AB 5500xl-W Genetic Analysis System, AB SOLiD 3 Plus System, AB SOLiD 4 System, AB SOLiD 4hq System, AB SOLiD PI System, AB SOLiD System, AB SOLiD System 2.0, AB SOLiD System 3.0, BGISEQ-50, BGISEQ-500, Complete Genomics, DNBSEQ-G400, DNBSEQ-G400 FAST, DNBSEQ-G50, DNBSEQ-T7, Element AVITI, GridION, Helicos HeliScope, HiSeq X Five, HiSeq X Ten, Illumina Genome Analyzer, Illumina Genome Analyzer II, Illumina Genome Analyzer IIx, Illumina HiScanSQ, Illumina HiSeq 1000, Illumina HiSeq 1500, Illumina HiSeq 2000, Illumina HiSeq 2500, Illumina HiSeq 3000, Illumina HiSeq 4000, Illumina HiSeq X, Illumina MiSeq, Illumina MiniSeq, Illumina NovaSeq 6000, Illumina NovaSeq X, Illumina iSeq 100, Ion GeneStudio S5, Ion GeneStudio S5 Plus, Ion GeneStudio S5 Prime, Ion Torrent Genexus, Ion Torrent PGM, Ion Torrent Proton, Ion Torrent S5, Ion Torrent S5 XL, MGISEQ-2000RS, MinION, NextSeq 1000, NextSeq 2000, NextSeq 500, NextSeq 550, Onso, PacBio RS, PacBio RS II, PromethION, Revio, Sequel, Sequel II, Sequel IIe, UG 100, unspecified |  will get values from the sra.experiment_xml |
| sequencing_protocol | A rule which guides how an activity should be performed. This is for the sequencing related[NCIT] | False | A URL from protocol.io |  | if multiple protocols. use a pipe to delimited |
