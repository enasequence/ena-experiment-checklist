# test script for the validation



schema_file=/Users/woollard/projects/easi-genomics/ExperimentChecklist/data/schema//TEST_type_schema.json

json_file=/Users/woollard/projects/easi-genomics/ExperimentChecklist/data/output_test/real_testing/TEST_type_works.json
echo $schema_file
echo $json_file
node /Users/woollard/projects/biovalidator/biovalidator/src/biovalidator.js  -d $json_file -s $schema_file

exit

json_file=/Users/woollard/projects/easi-genomics/ExperimentChecklist/data/output_test/real_testing/TEST_type_fails.json
node /Users/woollard/projects/biovalidator/biovalidator/src/biovalidator.js  -d $json_file -s $schema_file
