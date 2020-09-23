import sys
import os
import esprima
from multiprocessing import Manager
import itertools
from multiprocessing import Pool as ThreadPool
import multiprocessing
# import jsonpickle
# import pickle
import dill

import utilities

def get_ast(script_addr, write_addr):
    try:
        print('Processing: ', script_addr.split('/')[-1])
        script_text = utilities.read_full_file(script_addr)
        ast = esprima.parseScript(script_text, options = {'tolerant' : True}).toDict()
        utilities.write_dill_compressed(os.path.join(write_addr, script_addr.split('/')[-1] + '.json'), ast)
        utilities.append_file('ast_construction.log', script_addr.split('/')[-1] + ' Passed')
    except Exception as ex:
        print("Error while creating AST", str(ex))
        utilities.append_file('ast_construction.log', script_addr.split('/')[-1] + ' Failed')

def create_ast(unpacked_scripts_directory, ast_write_directory, cpu_to_relax = 1):
    # TO IGNORE
    # 256739_8e7c4c50ea6c91be2a239042a5c7006b
    all_unpacked_files = utilities.get_files_in_a_directory(unpacked_scripts_directory)
    raw_completed_unpacked_files = utilities.get_files_in_a_directory(ast_write_directory)
    completed_unpacked_files = []
    
    for unpacked in raw_completed_unpacked_files:
        completed_unpacked_files.append(unpacked.split('/')[-1])
    
    raw_completed_unpacked_files = []
    remaining_unpacked_files = []

    if os.path.isfile('ast_construction.log'):
        raw_processed = utilities.read_file('ast_construction.log')
    else:
        raw_processed = []

    processed_log = set()
    for item in raw_processed:
        processed_log.add(item.split(' ')[0])

    raw_processed = []

    for unpacked in all_unpacked_files:
        if unpacked.split('/')[-1] + '.json' in completed_unpacked_files or unpacked.split('/')[-1] == '256739_8e7c4c50ea6c91be2a239042a5c7006b': # or unpacked.split('/')[-1] in processed_log:
            continue
        else:
            remaining_unpacked_files.append(unpacked)
    
    completed_unpacked_files = []
    all_unpacked_files = []
    processed_log = set()

    print(len(remaining_unpacked_files))
    pool = ThreadPool(processes=multiprocessing.cpu_count() - cpu_to_relax)
    results = pool.starmap(get_ast, zip(remaining_unpacked_files, itertools.repeat(ast_write_directory)))
    pool.close()
    pool.join()
    
    # for f_name in remaining_unpacked_files[:20]:
    #     get_ast(f_name, ast_write_directory)
    
    # get_ast('/Users/uiqbal/Documents/work/data/unpacked_scripts/175960_5b84aace055ba4423d9cfeebe662de1e', ast_write_directory)
    
def main():
    unpacked_scripts_directory = sys.argv[1]
    ast_write_directory = sys.argv[2]
    cpu_to_relax = int(sys.argv[3])

    if not os.path.exists(ast_write_directory):
        os.makedirs(ast_write_directory)

    create_ast(unpacked_scripts_directory, ast_write_directory, cpu_to_relax)

if __name__ == '__main__':
    main()