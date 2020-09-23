import json
import queue
import sys
import os
from multiprocessing import Manager
import itertools
from multiprocessing import Pool as ThreadPool
import multiprocessing

import utilities

ALL = 'ALL'
NO_NAMES = 'NO_NAMES'
KEYWORD = 'KEYWORD'


def new_walk_no_names(all_data_addr, features_directory):
    node_queue = queue.Queue()
    all_data = utilities.read_json_compressed(all_data_addr)
    node_queue.put(('', all_data))

    node_list = []
    context_list = []
    text_list = []
    raw_features = set()
    first_run = True

    while not node_queue.empty():
        parent, data = node_queue.get()

        for key, value in data.items():
            if isinstance(value, dict):
                node_list.append(value)
            elif isinstance(value, list) or isinstance(value, tuple):
                if len(value) != 0:
                    for v in value:
                        node_list.append(v)
            else:
                if key == 'type':
                    context_list.append(value)
                elif key != 'name':
                    text_list.append(value)

        for context in context_list:
            for node in node_list:
                if node is not None:
                    node_queue.put((context, node))

        if first_run is False:
            for text in text_list:
                raw_features.add(str(parent) + ':' + ''.join(str(text).replace('\"', '').replace('\'', '').strip().replace(',', '').replace('\t', '').replace('\n', '').replace('\r', '').splitlines()))

        for context in context_list:
            for text in text_list:
                raw_features.add(str(context) + ':' + ''.join(str(text).replace('\"', '').replace('\'', '').strip().replace(',', '').replace('\t', '').replace('\n', '').replace('\r', '').splitlines()))

        node_list = []
        context_list = []
        text_list = []
        first_run = False

    utilities.write_list_compressed(os.path.join(features_directory, all_data_addr.split('/')[-1].replace('json', 'txt')), raw_features)


def new_walk_reserved_words(all_data_addr, features_directory, reserved_words):
    try:
        print('Processing: ', all_data_addr.split('/')[-1])
    
        node_queue = queue.Queue()
        all_data = utilities.read_dill_compressed(all_data_addr)
        # all_data = utilities.read_dill(all_data_addr)
        node_queue.put(('', all_data))

        node_list = []
        context_list = []
        text_list = []
        raw_features = set()
        first_run = True

        while not node_queue.empty():
            parent, data = node_queue.get()

            for key, value in data.items():
                if isinstance(value, dict):
                    node_list.append(value)
                elif isinstance(value, list) or isinstance(value, tuple):
                    if len(value) != 0:
                        for v in value:
                            node_list.append(v)
                else:
                    if key == 'type':
                        context_list.append(value)
                    else:
                        value_to_add = ''.join(str(value).replace('\"', '').replace('\'', '').strip().replace(',', '').replace('\t', '').replace('\n', '').replace('\r', '').splitlines()).strip()
                        if value_to_add in reserved_words:
                            text_list.append(value_to_add)

            for context in context_list:
                for node in node_list:
                    if node is not None:
                        node_queue.put((context, node))

            if first_run is False:
                for text in text_list:
                    raw_features.add(str(parent) + ':' + text)

            for context in context_list:
                for text in text_list:
                    raw_features.add(str(context) + ':' + text)

            node_list = []
            context_list = []
            text_list = []
            first_run = False

        utilities.write_list_compressed(os.path.join(features_directory, all_data_addr.split('/')[-1].replace('json', 'txt')), raw_features)
        utilities.append_file('ast_parsing.log', all_data_addr.split('/')[-1] + ' Passed')
        # utilities.write_list_simple(os.path.join(features_directory, all_data_addr.split('/')[-1].replace('json', 'txt')), raw_features)
    except Exception as e:
        print('Error while processing: ', all_data_addr.split('/')[-1], str(e))
        utilities.append_file('ast_parsing.log', all_data_addr.split('/')[-1] + ' Failed')
    except EOFError as er:
        print('Error while processing: ', all_data_addr.split('/')[-1], str(er))
        utilities.append_file('ast_parsing.log', all_data_addr.split('/')[-1] + ' Failed')

def new_walk(all_data_addr, features_directory):
    node_queue = queue.Queue()
    all_data = utilities.read_json_compressed(all_data_addr)
    node_queue.put(('', all_data))

    node_list = []
    context_list = []
    text_list = []
    raw_features = set()
    first_run = True

    while not node_queue.empty():
        parent, data = node_queue.get()

        for key, value in data.items():
            if isinstance(value, dict):
                node_list.append(value)
            elif isinstance(value, list) or isinstance(value, tuple):
                if len(value) != 0:
                    for v in value:
                        node_list.append(v)
            else:
                if key == 'type':
                    context_list.append(value)
                else:
                    text_list.append(value)

        for context in context_list:
            for node in node_list:
                if node is not None:
                    node_queue.put((context, node))

        if first_run is False:
            for text in text_list:
                raw_features.add(str(parent) + ':' + ''.join(str(text).replace('\"', '').replace('\'', '').strip().replace(',', '').replace('\t', '').replace('\n', '').replace('\r', '').splitlines()))

        for context in context_list:
            for text in text_list:
                raw_features.add(str(context) + ':' + ''.join(str(text).replace('\"', '').replace('\'', '').strip().replace(',', '').replace('\t', '').replace('\n', '').replace('\r', '').splitlines()))

        node_list = []
        context_list = []
        text_list = []
        first_run = False

    utilities.write_list_compressed(os.path.join(features_directory, all_data_addr.split('/')[-1].replace('json', 'txt')), raw_features)


def extract_features(directory_path, result_path, keywords_file, feature_type_to_read):
    all_files = utilities.get_files_in_a_directory(directory_path)
    temp = utilities.read_file(keywords_file)

    keywords_list = []
    for item in temp:
        keywords_list.append(item.strip())

    for f_name in all_files:
        try:
            file_data =  utilities.read_json(f_name)
            if feature_type_to_read == ALL:
                raw_features = new_walk(file_data)
            elif feature_type_to_read == NO_NAMES:
                raw_features = new_walk_no_names(file_data)
            elif feature_type_to_read == KEYWORD:
                raw_features = new_walk_reserved_words(file_data, keywords_list)

            utilities.append_list(f_name.replace(directory_path,result_directory).replace('json', 'txt'), raw_features)
        except Exception as e:
            print(f_name)
            print(str(e))

    return


def extract_features_multiprocess(ast_directory, features_directory, feature_type_to_extract, js_keywords_file, cpu_to_relax):
    all_files = utilities.get_files_in_a_directory(ast_directory)
    temp = utilities.read_file(js_keywords_file)

    keywords_list = []
    for item in temp:
        keywords_list.append(item.strip())

    raw_extracted_files = utilities.get_files_in_a_directory(features_directory)
    completed_feature_files = []
    
    for unpacked in raw_extracted_files:
        completed_feature_files.append(unpacked.split('/')[-1].split('.')[0])
    
    raw_extracted_files = []
    remaining_unpacked_files = []

    if os.path.isfile('ast_parsing.log'):
        raw_processed = utilities.read_file('ast_parsing.log')
    else:
        raw_processed = []

    processed_log = set()
    for item in raw_processed:
        processed_log.add(item.split(' ')[0].split('.')[0])

    raw_processed = []

    for unpacked in all_files:
        if unpacked.split('/')[-1].split('.')[0] in completed_feature_files: # or unpacked.split('/')[-1].split('.')[0] in processed_log:
            continue
        else:
            remaining_unpacked_files.append(unpacked)
    
    completed_feature_files = []
    all_files = []
    processed_log = set()

    print(len(remaining_unpacked_files), 'files to process')
    pool = ThreadPool(processes=multiprocessing.cpu_count() - cpu_to_relax)

    try:
        if feature_type_to_extract == ALL:
            results = pool.starmap(new_walk, zip(all_files, itertools.repeat(features_directory)))
        elif feature_type_to_extract == NO_NAMES:
            results = pool.starmap(new_walk_no_names, zip(all_files, itertools.repeat(features_directory)))
        elif feature_type_to_extract == KEYWORD:
            results = pool.starmap(new_walk_reserved_words, zip(remaining_unpacked_files, itertools.repeat(features_directory), itertools.repeat(keywords_list)))
        
        # for f_name in all_files:
        #     new_walk_reserved_words(f_name, features_directory, keywords_list)
        # utilities.append_list(f_name.replace(directory_path,result_directory).replace('json', 'txt'), raw_features)
    except Exception as e:
        print ('Exception in main thread: ', str(e))

    pool.close()
    pool.join()

    return

def main():
    ast_directory = sys.argv[1]
    features_directory = sys.argv[2]
    feature_type_to_extract = sys.argv[3]
    js_keywords_file = sys.argv[4]
    cpu_to_relax = int(sys.argv[5])

    if not os.path.exists(features_directory):
        os.makedirs(features_directory)
    
    extract_features_multiprocess(ast_directory, features_directory, feature_type_to_extract, js_keywords_file, cpu_to_relax)

if __name__ == '__main__':
    main()


# base_directory = '/media/umar/Elements/working_directory/processed_scripts'
# # # For ALL : START
# # result_directory = '/media/umar/Elements/working_directory/features_per_script'
# # js_keywords = '/media/umar/Elements/working_directory/JS_ALL_KEYWORDS.txt'
# # extract_features(base_directory, result_directory, js_keywords, ALL) 
# # # For ALL : END

# # # For NO_NAMES : START
# # result_directory = '/media/umar/Elements/working_directory/features_per_script_noname'
# # js_keywords = '/media/umar/Elements/working_directory/JS_ALL_KEYWORDS.txt'
# # extract_features(base_directory, result_directory, js_keywords, NO_NAMES) 
# # # For NO_NAMES : START

# # For KEYWORD : START
# result_directory = '/media/umar/Elements/working_directory/features_per_script_keyword'
# js_keywords = '/media/umar/Elements/working_directory/JS_ALL_KEYWORDS.txt'
# extract_features(base_directory, result_directory, js_keywords, KEYWORD) 
# # For KEYWORD : END