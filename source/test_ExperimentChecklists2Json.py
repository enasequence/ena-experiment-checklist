#!/usr/bin/env python3
import unittest
from icecream import ic
#ic.disable()
import sys
from attr import define

import ExperimentChecklists2Json
from ExperimentChecklists2Json import *

class TestExperimentChecklists2Json(unittest.TestCase):

    def test_get_config_data(self):
        ic()
        debug_status = True
        config_data = ExperimentChecklists2Json.read_config(debug_status)
        # ic(config_data)
        self.assertEqual(config_data["adapter_fields"]["adapters"], "")
        return config_data


    def set_expt_type_obj(self, experiment_type_obj):
        ic()
        ic(experiment_type_obj)
        self._experiment_type_obj = experiment_type_obj
        ic(self._experiment_type_obj)
        ic(self._experiment_type_obj.experiment_type_name)
        ic()
        um = self.get_expt_type_obj()
        ic(um.experiment_type_name)
        ic()

    def get_expt_type_obj(self):
        ic()
        ic(self)
        experiment_type_obj = self._experiment_type_obj
        ic(experiment_type_obj)
        ic(experiment_type_obj.experiment_type_name)
        ic()
        return experiment_type_obj


    def test_expt_init(self):
        ic()
        print("inside test_expt_init<----------------------")
        config_data = self.test_get_config_data()
        expt_objects = ExperimentChecklists2Json.process_and_get_fields(config_data)
        self.assertEqual(len(expt_objects), 1)
        for expt_type in expt_objects:
            print("\t",expt_type)
            ic()
            expt_object = expt_objects[expt_type]
            ic(expt_object)
            #self.assertIsInstance(expt_object, type(ExperimentType))
            ic(expt_object.experiment_type_name)
            self.assertEqual(expt_object.experiment_type_name, 'TEST_type')
            self.examine_expt_object(expt_object)
            self.set_expt_type_obj(expt_object)
            global global_exp_type_obj
            global_exp_type_obj = expt_object
            break
        ic()

    def test_expt_obj(self):
        ic()
        print("inside test_expt_objs<----------------------")
        expt_type_obj = global_exp_type_obj
        self.assertEqual(expt_type_obj.experiment_type_name, 'TEST_type')
        ic()
        ic(expt_type_obj.get_special_fields_list())
        test_list = ['pcr_fields', 'target_fields', 'multiplex_fields', 'adapter_fields']
        self.assertListEqual(expt_type_obj.get_special_fields_list(), test_list)
        test_dict = {'adapters': '',  'multiplex_identifiers': '',
                                       'pcr_primers': {'fwd_name': '', 'fwd_seq': '', 'rev_name': '', 'rev_seq': ''},
                                       'pcr_protocol': '',
                                       'target_loci': '',
                                       'target_subfragment': ''}
        self.assertDictContainsSubset(expt_type_obj.get_special_dict(), test_dict)
        test_dict = {'adapters': '',
                                   'checklist_group': 'TEST_group',
                                   'checklist_id': 'EXC00000Z',
                                   'checklist_name': 'TEST_name',
                                   'checklist_version': '20221129',
                                   'experiment_type': 'TEST_type',
                                   'library_source': 'TRANSCRIPTOMIC',
                                   'multiplex_identifiers': '',
                                   'pcr_primers': {'fwd_name': '', 'fwd_seq': '', 'rev_name': '', 'rev_seq': ''},
                                   'pcr_protocol': '',
                                   'target_loci': '',
                                   'target_subfragment': ''}
        self.assertDictContainsSubset(expt_type_obj.get_all_dict(), test_dict)

        ic()
        #sys.exit()

    def test_schema_objs(self):
        print("inside test_schema_objs<----------------------")
        config_data = self.test_get_config_data()
        expt_objects = ExperimentChecklists2Json.process_and_get_fields(config_data)
        schema_obj_dict = ExperimentChecklists2Json.create_schema_objects(expt_objects, config_data)
        for expt_type_name in schema_obj_dict:
            ic(expt_type_name)
            schema_obj = schema_obj_dict[expt_type_name]
            ic(schema_obj.experiment_type_name)
            self.assertEqual(schema_obj.experiment_type_name, "TEST_type")

            experiment_specific_dict = {'checklist_group': {'_example': 'TEST_group',
                             'default': 'TEST_group',
                             'description': '',
                             'type': 'string'},
         'checklist_id': {'_example': 'EXC00000Z',
                          'default': 'EXC00000Z',
                          'description': '',
                          'type': 'string'},
         'checklist_name': {'_example': 'TEST_name',
                            'default': 'TEST_name',
                            'description': '',
                            'type': 'string'},
         'checklist_version': {'_example': '20221129',
                               'default': '20221129',
                               'description': '',
                               'type': 'string'},
         'experiment_type': {'_example': 'TEST_type',
                             'default': 'TEST_type',
                             'description': '',
                             'type': 'string'},
         'library_source': {'_example': 'TRANSCRIPTOMIC',
                            'default': 'TRANSCRIPTOMIC',
                            'description': '',
                            'type': 'string'}}

            self.assertDictContainsSubset(schema_obj.get_experiment_specific_dict(), experiment_specific_dict)

            #print(schema_obj.get_json_schema())
            test_json_schema = {'checklists': {'checklist_fields_core': {'allOf': {
                'checklist_id': {'description': '', 'default': 'EXC00000Z', '_example': 'EXC00000Z', 'type': 'string'},
                'checklist_name': {'description': '', 'default': 'TEST_name', '_example': 'TEST_name',
                                   'type': 'string'},
                'checklist_group': {'description': '', 'default': 'TEST_group', '_example': 'TEST_group',
                                    'type': 'string'},
                'checklist_version': {'description': '', 'default': '20221129', '_example': '20221129',
                                      'type': 'string'},
                'experiment_type': {'description': '', 'default': 'TEST_type', '_example': 'TEST_type',
                                    'type': 'string'},
                'library_source': {'description': '', 'default': 'TRANSCRIPTOMIC', '_example': 'TRANSCRIPTOMIC',
                                   'type': 'string'}}, 'properties': {
                '_comment': 'This is an experiment attribute checklist template in JSON format. Please see https://github.com/Woolly-at-EBI/ExperimentChecklist/blob/main/docs/ExperimentChecklistDoc.html (NEED A PUBLIC URL) for details of what is mandatory and the allowable controlled vocabulary.',
                '_comment2': "This template allows 1 or more experiments' metadata to be submitted. If >1 experiments: in JSON style, please add a comma at the end of the previous record just after the closing }.",
                'study_id': {'description': '', 'default': 'my study', 'type': 'string'}, 'sample_accession': {
                    'description': 'This is the study accession number that starts with ERP granted after registering a study with the ENA. [ENA]',
                    'type': 'string'}, 'experiment_name': {
                    'description': 'A unique name of the experiment within your study. An experiment is the sequencing activity that generates one or more sequencing runs on a specific sample. [ENA]',
                    'default': 'my lovely TRANSCRIPTOMICS experiment', 'type': 'string'}, 'library_source': {
                    'description': 'The LIBRARY_SOURCE specifies the type of source material that is being sequenced. [INSDC]',
                    'default': 'TRANSCRIPTOMICS---',
                    'enum': ['GENOMIC SINGLE CELL', 'GENOMIC', 'METAGENOMIC', 'METATRANSCRIPTOMIC', 'OTHER',
                             'SYNTHETIC', 'TRANSCRIPTOMIC SINGLE CELL', 'TRANSCRIPTOMIC', 'VIRAL RNA'],
                    'type': 'string'},
                'library_strategy': {'description': 'Sequencing technique intended for this library.[INSDC]',
                                     'default': 'RNA-Seq',
                                     'enum': ['AMPLICON', 'ATAC-seq', 'Bisulfite-Seq', 'CLONE', 'CLONEEND', 'CTS',
                                              'ChIA-PET', 'ChIP-Seq', 'DNase-Hypersensitivity', 'EST', 'FAIRE-seq',
                                              'FINISHING', 'FL-cDNA', 'Hi-C', 'MBD-Seq', 'MNase-Seq', 'MRE-Seq',
                                              'MeDIP-Seq', 'OTHER', 'POOLCLONE', 'RAD-Seq', 'RIP-Seq', 'RNA-Seq',
                                              'SELEX', 'Synthetic-Long-Read', 'Targeted-Capture',
                                              'Tethered Chromatin Conformation Capture', 'Tn-Seq', 'VALIDATION', 'WCS',
                                              'WGA', 'WGS', 'WXS', 'miRNA-Seq', 'ssRNA-seq'], 'type': 'string'},
                'library_selection': {
                    'description': 'Method used to enrich the target in the sequence library preparation. [INSDC]',
                    'default': 'unspecified',
                    'enum': ['5-methylcytidine antibody', 'CAGE', 'ChIP', 'ChIP-Seq', 'DNase', 'HMPR',
                             'Hybrid Selection', 'Inverse rRNA selection', 'Inverse rRNA', 'MDA', 'MF', 'MNase', 'MSLL',
                             'Oligo-dT', 'PCR', 'PolyA', 'RACE', 'RANDOM PCR', 'RANDOM', 'RT-PCR',
                             'Reduced Representation', 'Restriction Digest', 'cDNA', 'cDNA_oligo_dT',
                             'cDNA_randomPriming', 'other', 'padlock probes capture method', 'size fractionation',
                             'unspecified'], 'type': 'string'},
                'library_name': {'description': 'The name of the nucleotide sequencing library. [NCIT]',
                                 'type': 'string'}, 'library_description': {
                    'description': 'The free descrqqgreo iption of the nucleotide sequencing library. [NCIT adapted]',
                    'type': 'string'}, 'insert_size': {'default': 0,
                                                       'description': 'The average insert size found during nucleic acid sequencing. [NCIT]',
                                                       'type': 'number'}, 'instrument_platform': {
                    'description': 'The name of the technology platform used to perform nucleic acid sequencing. [NCIT]',
                    '_example': 'ILLUMINA', 'default': 'ILLUMINA',
                    'enum': ['BGISEQ', 'CAPILLARY', 'DNBSEQ', 'ILLUMINA', 'ION_TORRENT', 'LS454', 'OXFORD_NANOPORE',
                             'PACBIO_SMRT'], 'type': 'string'}, 'instrument_model': {
                    'description': 'The name and/or number associated with a specific sequencing instrument model.  [NCIT-adapted]',
                    '_example': 'llumina MiSeq', 'default': 'unspecified',
                    'enum': ['454 GS 20', '454 GS FLX Titanium', '454 GS FLX', '454 GS FLX+', '454 GS Junior', '454 GS',
                             'AB 310 Genetic Analyzer', 'AB 3130 Genetic Analyzer', 'AB 3130xL Genetic Analyzer',
                             'AB 3500 Genetic Analyzer', 'AB 3500xL Genetic Analyzer', 'AB 3730 Genetic Analyzer',
                             'AB 3730xL Genetic Analyzer', 'BGISEQ-500', 'DNBSEQ-G400 FAST', 'DNBSEQ-G400',
                             'DNBSEQ-G50', 'DNBSEQ-T7', 'GridION', 'HiSeq X Five', 'HiSeq X Ten',
                             'Illumina Genome Analyzer II', 'Illumina Genome Analyzer IIx', 'Illumina Genome Analyzer',
                             'Illumina HiScanSQ', 'Illumina HiSeq 1000', 'Illumina HiSeq 1500', 'Illumina HiSeq 2000',
                             'Illumina HiSeq 2500', 'Illumina HiSeq 3000', 'Illumina HiSeq 4000', 'Illumina MiSeq',
                             'Illumina MiniSeq', 'Illumina NovaSeq 6000', 'Illumina iSeq 100', 'Ion Torrent PGM',
                             'Ion Torrent Proton', 'Ion Torrent S5 XL', 'Ion Torrent S5', 'MinION', 'NextSeq 500',
                             'NextSeq 550', 'PacBio RS II', 'PacBio RS', 'PromethION', 'Sequel', 'unspecified'],
                    'type': 'string'}}}}, '$id': 'https://www.ebi.ac.uk/exeriment.checklist.ena.schema.json',
             '$schema': 'http://json-schema.org/draft-07/schema#',
             'title': 'PROTOTYPE Experimental Checklists JSON schema',
             'description': 'Contained herein are the specific ENO experimental JSON schema describing what is need to validate specific checklists',
             'type': 'object'}
            self.assertDictContainsSubset(schema_obj.get_json_schema(), test_json_schema)




    def examine_expt_object(self, expt_object):
        ic()
        self._expt_object = expt_object
        ic(self._expt_object)




if __name__ == '__main__':
    ic("do some testing")
    sys.exit()
    # unittest.main()
