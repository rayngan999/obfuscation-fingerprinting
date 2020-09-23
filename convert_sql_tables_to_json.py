import sqlite3
import json
import sys
import os
from tqdm import tqdm

import utilities


def convert_to_json(db_addr, data_directory, file_name, partition_size = 10000):
    con = sqlite3.connect(db_addr)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT MAX(id) as max_id FROM javascript")
    total_rows = cur.fetchone()['max_id']
    pbar = tqdm(total=total_rows)
    cur.execute('SELECT visit_id, script_url, top_level_url, symbol, arguments, value, script_line, script_col FROM javascript')

    js_data = {}
    # unique_scripts_keymap = {}

    id_index = 0
    # key_counter = 0 
    id_key_map = {}   
    # unique_scripts = []
    current_partition_index = 1
    required_partition_index = 1
    next_partition_index = 1
    next_check = True

    for row in cur:         
        str_id = str(row[0]) + '|' + row[2] + '|' + row[1]    

        if str_id not in id_key_map:
            if next_partition_index != current_partition_index:
                # check if the file exists read from there, otherwise create a new file/object
                utilities.write_json(os.path.join(data_directory, file_name + '_partition_' + str(current_partition_index) + '.json'), js_data, indent_length=0)
                if os.path.exists(os.path.join(data_directory, file_name + '_partition_' + str(next_partition_index) + '.json')):
                    js_data = utilities.read_json(os.path.join(data_directory, file_name + '_partition_' + str(next_partition_index) + '.json'))
                    print('39: Writing:', file_name + '_partition_' + str(current_partition_index), 'Reading:', file_name + '_partition_' + str(next_partition_index), 'Next Partition: ', next_partition_index)
                else:
                    print('39: Writing:', file_name + '_partition_' + str(current_partition_index), 'Not Reading:', file_name + '_partition_' + str(next_partition_index), 'Next Partition: ', next_partition_index)
                current_partition_index = next_partition_index
                next_check = True

            id_index += 1
            str_id_index = str(id_index)   
            id_key_map[str_id] = {}
            id_key_map[str_id]['id_index'] = str_id_index

            id_key_map[str_id]['partition_index'] = current_partition_index
            js_data[str_id_index] = {}
            js_data[str_id_index]['information'] = []
        else:
            str_id_index = id_key_map[str_id]['id_index']
            required_partition_index = id_key_map[str_id]['partition_index']

            if required_partition_index != current_partition_index:
                utilities.write_json(os.path.join(data_directory, file_name + '_partition_' + str(current_partition_index) + '.json'), js_data, indent_length=0)
                js_data = utilities.read_json(os.path.join(data_directory, file_name + '_partition_' + str(required_partition_index) + '.json'))
                print('58: Writing:', file_name + '_partition_' + str(current_partition_index), 'Reading:', file_name + '_partition_' + str(required_partition_index), 'Next Partition: ', next_partition_index)
                current_partition_index = required_partition_index
            # make sure we have the right json object for the partition

        js_data[str_id_index]['visit_id'] = row[0]
        js_data[str_id_index]['top_url'] = row[2]
        js_data[str_id_index]['script_url'] = row[1]
        js_data[str_id_index]['script_line'] = row[6]
        js_data[str_id_index]['script_col'] = row[7]
        js_data[str_id_index]['information'].append({'symbol':row[3], 'argument':row[4], 'value':row[5]})

        if id_index % partition_size == 0:
            # Because you may not update id_index and might still read rows before the partition.
            # if not os.path.exists(os.path.join(data_directory, file_name + '_partition_' + str(next_partition_index) + '.json')):
            if next_check:
                utilities.write_json(os.path.join(data_directory, file_name + '_partition_' + str(next_partition_index) + '.json'), js_data, indent_length=0)
                next_partition_index += 1
                print('76: Writing:', file_name + '_partition_' + str(current_partition_index), 'Next Partition: ', next_partition_index)
                current_partition_index = next_partition_index
                required_partition_index = next_partition_index
                js_data = {}
                next_check = False               

        pbar.update(1)
    utilities.write_json(os.path.join(data_directory, 'mapping.json'), id_key_map, indent_length=4)
    return 

def convert_to_json_simple(db_addr, data_directory, file_name, partition_size = 10000):
    con = sqlite3.connect(db_addr)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT MAX(id) as max_id FROM javascript")
    total_rows = cur.fetchone()['max_id']
    pbar = tqdm(total=total_rows)
    cur.execute('SELECT visit_id, script_url, top_level_url, symbol, arguments, value, script_line, script_col FROM javascript')

    js_data = {}
    unique_scripts = []

    counter = 0 
    for row in cur:   
        counter += 1         
        str_id = str(row[0]) + '|' + row[2] + '|' + row[1]    
        
        try:
            id_index = unique_scripts.index(str_id)    
        except ValueError:
            id_index = len(unique_scripts)
            unique_scripts.append(str_id)        
            js_data[id_index] = {}
            js_data[id_index]['information'] = []
        
        js_data[id_index]['visit_id'] = row[0]
        js_data[id_index]['top_url'] = row[2]
        js_data[id_index]['script_url'] = row[1]
        js_data[id_index]['script_line'] = row[6]
        js_data[id_index]['script_col'] = row[7]
        js_data[id_index]['information'].append({'symbol':row[3], 'argument':row[4], 'value':row[5]})

        pbar.update(1)
    
    utilities.write_json(os.path.join(data_directory, file_name + '.json'), js_data, indent_length=0)
    return 


def convert_to_json_greedy(db_addr, data_directory, file_name, partition_size = 10000):
    con = sqlite3.connect(db_addr)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT MAX(id) as max_id FROM javascript")
    total_rows = cur.fetchone()['max_id']
    pbar = tqdm(total=total_rows)
    cur.execute('SELECT visit_id, script_url, top_level_url, symbol, arguments, value, script_line, script_col FROM javascript')

    js_data = {}
    remaining_js_data = {}

    id_index = 0
    id_key_map = {}   
    current_partition_index = 1
    check_status = True

    for row in cur:         
        str_id = str(row[0]) + '|' + row[2] + '|' + row[1]    

        if str_id not in id_key_map:
            id_index += 1
            str_id_index = str(id_index)   
            id_key_map[str_id] = {}
            id_key_map[str_id]['id_index'] = str_id_index

            id_key_map[str_id]['partition_index'] = current_partition_index
            js_data[str_id_index] = {}
            js_data[str_id_index]['information'] = []
            check_status = True
            update_json_data = True
        else:
            str_id_index = id_key_map[str_id]['id_index']
            required_partition_index = id_key_map[str_id]['partition_index']

            if required_partition_index != current_partition_index:
                if required_partition_index not in remaining_js_data:
                    remaining_js_data[required_partition_index] = {}
                    remaining_js_data[required_partition_index][str_id_index] = {}
                    remaining_js_data[required_partition_index][str_id_index]['information'] = []
                else:
                    if str_id_index not in remaining_js_data[required_partition_index]:
                        remaining_js_data[required_partition_index][str_id_index] = {}
                        remaining_js_data[required_partition_index][str_id_index]['information'] = []

                remaining_js_data[required_partition_index][str_id_index]['visit_id'] = row[0]
                remaining_js_data[required_partition_index][str_id_index]['top_url'] = row[2]
                remaining_js_data[required_partition_index][str_id_index]['script_url'] = row[1]
                remaining_js_data[required_partition_index][str_id_index]['script_line'] = row[6]
                remaining_js_data[required_partition_index][str_id_index]['script_col'] = row[7]
                remaining_js_data[required_partition_index][str_id_index]['information'].append({'symbol':row[3], 'argument':row[4], 'value':row[5]})
                update_json_data = False
                        
            else:
                update_json_data = True
        
        if update_json_data:
            js_data[str_id_index]['visit_id'] = row[0]
            js_data[str_id_index]['top_url'] = row[2]
            js_data[str_id_index]['script_url'] = row[1]
            js_data[str_id_index]['script_line'] = row[6]
            js_data[str_id_index]['script_col'] = row[7]
            js_data[str_id_index]['information'].append({'symbol':row[3], 'argument':row[4], 'value':row[5]})

        if id_index % partition_size == 0:
            # Because you may not update id_index and might still read rows before the partition.
            # if not os.path.exists(os.path.join(data_directory, file_name + '_partition_' + str(current_partition_index) + '.json')):
            if check_status:
                utilities.write_json(os.path.join(data_directory, file_name + '_partition_' + str(current_partition_index) + '.json'), js_data, indent_length=0)
                print('76: Writing:', file_name + '_partition_' + str(current_partition_index), 'Next Partition: ', current_partition_index + 1)
                current_partition_index += 1
                js_data = {}    
                check_status = False  

        pbar.update(1)
    # In case rows are a perfect divisible of id_index % partition_size we will have an empty object. So It is okay.
    utilities.write_json(os.path.join(data_directory, file_name + '_partition_' + str(current_partition_index) + '.json'), js_data, indent_length=0)
    utilities.write_json(os.path.join(data_directory, 'remaining.json'), remaining_js_data, indent_length=0)
    utilities.write_json(os.path.join(data_directory, 'mapping.json'), id_key_map, indent_length=4)
    
    return 

def adjust_greedy(partitioned_data_directory, partitioned_file_name='javascript_partition_', remaining_file_name='remaining.json'):
    remaining_json = utilities.read_json(os.path.join(partitioned_data_directory, remaining_file_name))

    pbar_overall = tqdm(total=len(remaining_json))
    for key in remaining_json:
        current_json = utilities.read_json(os.path.join(partitioned_data_directory, partitioned_file_name + key + '.json'))

        for str_id_index in remaining_json[key]:
            if 'visit_id' not in remaining_json[key][str_id_index]:
                continue

            current_json[str_id_index]['visit_id'] = remaining_json[key][str_id_index]['visit_id']
            current_json[str_id_index]['top_url'] = remaining_json[key][str_id_index]['top_url']
            current_json[str_id_index]['script_url'] = remaining_json[key][str_id_index]['script_url']
            current_json[str_id_index]['script_line'] = remaining_json[key][str_id_index]['script_line']
            current_json[str_id_index]['script_col'] = remaining_json[key][str_id_index]['script_col']
            for item in remaining_json[key][str_id_index]['information']:
                current_json[str_id_index]['information'].append(item)
            
        utilities.write_json(os.path.join(partitioned_data_directory, partitioned_file_name + key + '_updated.json'), current_json, indent_length=0)
        pbar_overall.update(1)

    return

def update_hash(db_addr, partitioned_data_directory, mapping_file_name='mapping.json'):
    mapping_json = utilities.read_json(os.path.join(partitioned_data_directory, mapping_file_name))

    con = sqlite3.connect(db_addr)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT MAX(id) as max_id FROM http_responses")
    total_rows = cur.fetchone()['max_id']
    pbar = tqdm(total=total_rows)
    cur.execute('SELECT visit_id, url, content_hash FROM http_responses')
    
    updated_mapping_object = {}
    url_updated_mapping_object = {}
    total_keys_matched = 0

    for key in mapping_json:
        new_key = key.split('|',2)[0].strip() + '|' + key.split('|',2)[2].strip()
        updated_mapping_object[new_key] = {}
        updated_mapping_object[new_key]['old_key'] = key
        updated_mapping_object[new_key]['id_index'] = mapping_json[key]['id_index']
        updated_mapping_object[new_key]['partition_index'] = mapping_json[key]['partition_index']
        updated_mapping_object[new_key]['content_hash'] = ''
        
        mapping_json[key]['new_id_url_key'] = new_key

        new_key = key.split('|',2)[2].strip()
        url_updated_mapping_object[new_key] = {}
        url_updated_mapping_object[new_key]['old_key'] = key
        url_updated_mapping_object[new_key]['id_index'] = mapping_json[key]['id_index']
        url_updated_mapping_object[new_key]['partition_index'] = mapping_json[key]['partition_index']
        url_updated_mapping_object[new_key]['content_hash'] = ''

        mapping_json[key]['new_url_key'] = new_key
    
    for row in cur:
        if row[2] != '' and row[2] != None:
            db_row_key = str(row[0]) + '|' + row[1].strip() 
            if db_row_key in updated_mapping_object:
                updated_mapping_object[db_row_key]['content_hash'] = row[2].strip()
                total_keys_matched += 1
            if row[1].strip() != '' and row[1].strip() in url_updated_mapping_object:
                url_updated_mapping_object[row[1].strip()]['content_hash'] = row[2].strip()
                total_keys_matched += 1

                # if row[1].strip() != '':
                #     for key in updated_mapping_object:
                #         if key.split('|', 2)[1].strip() == row[1].strip():
                #             updated_mapping_object[key]['content_hash'] = row[2].strip()
                #             total_keys_matched += 1
                #             break
        pbar.update(1)
    print('Total keys matched:', total_keys_matched)
    utilities.write_json(os.path.join(partitioned_data_directory, 'mapping_updated.json'), updated_mapping_object, indent_length=0)
    utilities.write_json(os.path.join(partitioned_data_directory, 'url_only_mapping_updated.json'), url_updated_mapping_object, indent_length=0)

    for key in mapping_json:
        mapping_json[key]['content_hash'] = updated_mapping_object[mapping_json[key]['new_id_url_key']]['content_hash']
        if mapping_json[key]['content_hash'] == '':
            mapping_json[key]['content_hash'] = url_updated_mapping_object[mapping_json[key]['new_url_key']]['content_hash']

    utilities.write_json(os.path.join(partitioned_data_directory, 'mapping_with_hash.json'), mapping_json, indent_length=0)
    return

def update_hash_in_partitioned_files(data_directory, file_name, suffix_1='_partition_' , suffix_2='_updated', mapping_file_with_hash='mapping_with_hash.json'):
    mapping_json = utilities.read_json(os.path.join(data_directory, mapping_file_with_hash))

    dict_per_partition = {}
    empty = 0
    non_empty = 0
    pbar = tqdm(total=len(mapping_json))
    for key in mapping_json:
        if mapping_json[key]['partition_index'] not in dict_per_partition:
            dict_per_partition[mapping_json[key]['partition_index']] = {}
            dict_per_partition[mapping_json[key]['partition_index']][mapping_json[key]['id_index']] = {} 
        else:
            dict_per_partition[mapping_json[key]['partition_index']][mapping_json[key]['id_index']] = {}
        

        if mapping_json[key]['content_hash'].strip() == '':
            empty += 1
        else:
            non_empty += 1
        
        dict_per_partition[mapping_json[key]['partition_index']][mapping_json[key]['id_index']]['content_hash'] = mapping_json[key]['content_hash']

        pbar.update(1)
    print('empty, non-empty:', empty, non_empty)

    pbar = tqdm(total=len(dict_per_partition))
    for key in dict_per_partition:
        current_json = utilities.read_json(os.path.join(data_directory, file_name + suffix_1 + str(key) + suffix_2 + '.json'))
        for item in dict_per_partition[key]:
            current_json[item]['content_hash'] = dict_per_partition[key][item]['content_hash']
        utilities.write_json(os.path.join(data_directory, file_name + '_with_hash_partition_' + str(key) + '.json'), current_json)
        pbar.update(1)
    return

def main():
    db_addr = sys.argv[1]
    analysis_directory = sys.argv[2]
    data_directory = sys.argv[3]
    file_name = sys.argv[4]
    input_partition_size = int(sys.argv[5])

    if not os.path.exists(analysis_directory):
        print('Analysis directory does not exist.')
        return
    else:
        if not os.path.exists(os.path.join(analysis_directory, data_directory)):
            os.makedirs(os.path.join(analysis_directory, data_directory))
            data_directory = os.path.join(analysis_directory, data_directory)
        else:
            print('Data directory already exist, create a new one.')
            return


    # DO NOT RUN THESE : START
    # convert_to_json(db_addr, data_directory, file_name, partition_size = input_partition_size)
    # convert_to_json_simple(db_addr, data_directory, file_name, partition_size = input_partition_size)
    # DO NOT RUN THESE : END

    # MAY WANT TO DELETE PREVIOS FILES AFTER RUNNING GREEDY VERSION
    # ONLY THE GREEDY VERSION WORKS
    convert_to_json_greedy(db_addr, data_directory, file_name, partition_size = input_partition_size)
    adjust_greedy(data_directory)
    update_hash(db_addr, data_directory)
    update_hash_in_partitioned_files(data_directory, file_name)

if __name__ == '__main__':
    main()
