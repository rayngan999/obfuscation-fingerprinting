from collections import deque
import random
import os
import sys
from os import listdir
from os.path import isfile, join
from collections import defaultdict
from numpy import array
import numpy as np
import csv
import utilities
import re
from tqdm import tqdm


def get_features(feature_mapping_file):
    feature_mappings = utilities.read_file_newline_stripped(feature_mapping_file)
    feature_mappings_map = {}

    for feature in feature_mappings:
        feature_mappings_map[feature.strip().split(',',2)[1]] = feature.strip().split(',',2)[0]

    return feature_mappings_map


def create_feature_mapping(feature_mapping_file, parsed_ast_address, mapped_features_address):
    all_features = get_features(feature_mapping_file)
    all_files = utilities.get_files_in_a_directory(parsed_ast_address)
    
    pbar = tqdm(total=len(all_files))
    for f_name in all_files:
        f_content = utilities.read_list_compressed(f_name)

        feature_map_items = set()
        for item in f_content:
            if item.strip() in all_features:
                feature_map_items.add(all_features[item.strip()])

        utilities.write_list_compressed(os.path.join(mapped_features_address, f_name.split('/')[-1]), feature_map_items)
        pbar.update(1)
    return


def create_feature_csv_with_variance_and_class_labels(all_features, file_to_write, mapped_features_address):
    # Read top 1K features only
    feature_mapping = utilities.read_file_newline_stripped(all_features)

    str_to_write = 'id,hash,' + ','.join(feature_mapping) + ',class'
    utilities.append_file(file_to_write, str_to_write)
    print('Wrote CSV header')

    # Reading mapped feature files
    feature_files = utilities.get_files_in_a_directory(mapped_features_address)
    # count = 0

    # Dictionary initialization
    features_dictionary = defaultdict(lambda: {'index': len(features_dictionary)})
    for feature in feature_mapping:
        features_dictionary[feature]['info'] = 0

    positive_counter = 0
    # Reading malicious features
    pbar = tqdm(total=len(feature_files))

    # No need to assign label for training data
    label = '?'

    for f_name in feature_files:        
        file_content = set(utilities.read_list_compressed(f_name))
        try:
            row_id = f_name.split('/')[-1].split('_')[0].strip()
            script_hash = f_name.split('/')[-1].split('_')[1].split('.')[0].strip()

        except Exception as ex:
            print('Exception occured while spliting file name:', f_name)
            pbar.update(1)
            continue

        for raw_feature in file_content:
            features_dictionary[raw_feature]['info'] = 1

        str_to_write = row_id + ',' + script_hash 
        
        for feature in feature_mapping:
            str_to_write += ',' + str(features_dictionary[feature]['info'])
            features_dictionary[feature]['info'] = 0

        str_to_write += ',' + label
        utilities.append_file(file_to_write, str_to_write)

        pbar.update(1)

    return

def create_arff(csv_addr, arff_addr):
    csv_file = utilities.read_file(csv_addr)
    csv_columns = csv_file[0].split(',')

    with open(arff_addr, "a") as myfile:
        myfile.write('@relation keyword_features' + '\n')
        myfile.write('' + '\n')
        myfile.write('@attribute id numeric' + '\n')             
        myfile.write('@attribute hash string' + '\n')
        # myfile.write('@attribute similarity numeric' + '\n')
            
        for feature in csv_columns[2:-1]:            
            myfile.write('@attribute ' + feature + ' {0,1}' + '\n')             

        myfile.write('@attribute class {FP,NONFP}' + '\n')
        myfile.write('' + '\n')
        myfile.write('@data' + '\n')
        myfile.write('' + '\n')
        
        for line in csv_file[1:]:
            myfile.write(line)
    return


def main():
    features_directory = sys.argv[1]
    features_mapping_file_name = sys.argv[2]
    mapped_features_directory = sys.argv[3]
    top_1K_features = sys.argv[4]

    csv_file_name = 'static_features.csv'
    arff_file_name = 'static_features.arff'

    print('\nCreating feature mapping')
    create_feature_mapping(features_mapping_file_name, features_directory, mapped_features_directory)

    print('\nCreating CSV of features with calss label')
    create_feature_csv_with_variance_and_class_labels(top_1K_features, csv_file_name, mapped_features_directory)
    
    print('Creating ARFF')
    create_arff(csv_file_name, arff_file_name)

if __name__ == '__main__':
    main()
