# obfuscation-fingerprinting

:warning: Do not use the code as it is. You will have to tweak the code to adjust to your needs.

## Static Analysis 

1. Run extract_scripts_content.ipynb to extract scripts from OpenWPM
2. Use unpack_scripts_with_eval.py to unpack eval scripts 
3. You will need to rely on https://github.com/uiowa-irl/AdGraph to unpack eval
4. Create ASTs of extracted script scripts using create_ast.py
5. Parse ASTs using parse_ast.py
    1. ast_directory: directory which contains the ASTs generated in previous step
    2. features_directory: directory where you want to store features 
    3. feature_type_to_extract: specify keyword. I think I used keyword features in the final training. 
    4. js_keywords_file: it needs the JavaScript keywords. Provide cleaned_apis_unique.txt as input.
    5. cpu_to_relax: number of cpu's to relax. The code uses multiprocessing.


## Dynamic Analysis

### Conversion to JSON
The code is designed to work with JSON representation of OpenWPM's sqlite table. As a first step, please run **convert_sql_tables_to_json.py** to convert the data needed by FP-Inspector to json representation. 

convert_sql_tables_to_json.py takes input:
1. db_addr: address of OpenWPM's sqlite database.
2. analysis_directory: it is kind of a parent directory, which can have other data associated to the JSON representation.
3. data_directory: directory where you want to store the json representation.
4. file_name: name of the JSON file. Please note that several files will be created based on the partition size. 
5. input_partition_size: number of script executions you want to keep in each partition. Default is 10K

##
