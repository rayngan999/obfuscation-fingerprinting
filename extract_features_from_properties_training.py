###################################################
# cleanded up code from extract_propert_features.py
###################################################
import sys
import os
import json
import math 
from tqdm import tqdm

import utilities
import feature_dictionaries


def check_presence(processed_hashes, processed_urls, processed_urls_list, script_hash, script_url):
    if script_hash.strip() != '':
        if script_hash in processed_hashes:
            return True
        else:
            processed_hashes.add(script_hash)
    else:
        if script_url.strip() != '':
            if script_url.strip() in processed_urls:
                return True
            else:
                processed_urls.add(script_url.strip())
                processed_urls_list.append(script_url.strip())
        else:
            return True
    return False

def add_one_grams(one_grams, global_symbols_count):
    for key in global_symbols_count:
        one_grams[key] = 0

def create_header(global_symbols_count, feature_mapping):
    one_gram_header = []
    feature_header = []
    count = 0

    for key in global_symbols_count:
        feature_header.append('fog' + str(count))
        one_gram_header.append(key)
        count += 1

    for key in global_symbols_count:

        # For most of the custom argument values we use more than a single value
        if key == 'canvasrenderingcontext2d.fillrect':
            fm_keys = ['canvasrenderingcontext2d.fillrect-OnScreen', 
            'canvasrenderingcontext2d.fillrect-Size']
        elif key == 'canvasrenderingcontext2d.filltext':
            fm_keys = ['canvasrenderingcontext2d.filltext-TextSize', 
            'canvasrenderingcontext2d.filltext-OnScreen']
        elif key == 'canvasrenderingcontext2d.rect':
            fm_keys = ['canvasrenderingcontext2d.rect-OnScreen', 
            'canvasrenderingcontext2d.rect-Size']
        elif key == 'canvasrenderingcontext2d.arc':
            fm_keys = ['canvasrenderingcontext2d.arc-OnScreen', 
            'canvasrenderingcontext2d.arc-Size']
        elif key == 'canvasrenderingcontext2d.getimagedata':
            fm_keys = ['canvasrenderingcontext2d.getimagedata-OnScreen', 
            'canvasrenderingcontext2d.getimagedata-Size']
        elif key == 'canvasrenderingcontext2d.createradialgradient':
            fm_keys = ['canvasrenderingcontext2d.createradialgradient-OnScreen-One', 
            'canvasrenderingcontext2d.createradialgradient-OnScreen-Two',
            'canvasrenderingcontext2d.createradialgradient-Size-One',
            'canvasrenderingcontext2d.createradialgradient-Size-Two']
        elif key == 'canvasrenderingcontext2d.beziercurveto':
            fm_keys = ['canvasrenderingcontext2d.beziercurveto-OnScreen',
            'canvasrenderingcontext2d.beziercurveto-Size-One',
            'canvasrenderingcontext2d.beziercurveto-Size-Two']
        elif key == 'canvasrenderingcontext2d.stroketext':
            fm_keys = ['canvasrenderingcontext2d.stroketext-OnScreen',
            'canvasrenderingcontext2d.stroketext-TextSize']
        elif key == 'canvasrenderingcontext2d.strokerect':
            fm_keys = ['canvasrenderingcontext2d.strokerect-OnScreen',
            'canvasrenderingcontext2d.strokerect-Size']
        elif key == 'canvasrenderingcontext2d.arcto':
            fm_keys = ['canvasrenderingcontext2d.arcto-OnScreen',
            'canvasrenderingcontext2d.arcto-Size-One',
            'canvasrenderingcontext2d.arcto-Size-Two']
        elif key == 'audiocontext.createbuffer':
            fm_keys = ['audiocontext.createbuffer-NumChannels',
            'audiocontext.createbuffer-Length',
            'audiocontext.createbuffer-SampleRate']
        elif key == 'offlineaudiocontext.createscriptprocessor':
            fm_keys = ['offlineaudiocontext.createscriptprocessor-BufferSize',
            'offlineaudiocontext.createscriptprocessor-InNumChannels',
            'offlineaudiocontext.createscriptprocessor-OutNumChannels']
        elif key == 'audiocontext.createscriptprocessor':
            fm_keys = ['audiocontext.createscriptprocessor-BufferSize',
            'audiocontext.createscriptprocessor-InNumChannels',
            'audiocontext.createscriptprocessor-OutNumChannels']
        elif key == 'canvasrenderingcontext2d.clearrect':
            fm_keys = ['canvasrenderingcontext2d.clearrect-OnScreen', 
            'canvasrenderingcontext2d.clearrect-Size']
        elif key == 'canvasrenderingcontext2d.quadraticcurveto':
            fm_keys = ['canvasrenderingcontext2d.quadraticcurveto-OnScreen', 
            'canvasrenderingcontext2d.quadraticcurveto-Size']
        elif key == 'webglrenderingcontext.bufferdata':
            fm_keys = ['webglrenderingcontext.bufferdata-First',
            'webglrenderingcontext.bufferdata-Last']
        elif key == 'webglrenderingcontext.uniform2f':
            fm_keys = ['webglrenderingcontext.uniform2f-Second',
            'webglrenderingcontext.uniform2f-Third']
        elif key == 'webgl2renderingcontext.uniform2f':
            fm_keys = ['webgl2renderingcontext.uniform2f-Second',
            'webgl2renderingcontext.uniform2f-Third']
        elif key == 'webglrenderingcontext.vertexattribpointer':
            fm_keys = ['webglrenderingcontext.vertexattribpointer-First',
            'webglrenderingcontext.vertexattribpointer-Second',
            'webglrenderingcontext.vertexattribpointer-Third',
            'webglrenderingcontext.vertexattribpointer-Fourth',
            'webglrenderingcontext.vertexattribpointer-Fifth',
            'webglrenderingcontext.vertexattribpointer-Sixth']
        elif key == 'webgl2renderingcontext.vertexattribpointer':
            fm_keys = ['webgl2renderingcontext.vertexattribpointer-First',
            'webgl2renderingcontext.vertexattribpointer-Second',
            'webgl2renderingcontext.vertexattribpointer-Third',
            'webgl2renderingcontext.vertexattribpointer-Fourth',
            'webgl2renderingcontext.vertexattribpointer-Fifth',
            'webgl2renderingcontext.vertexattribpointer-Sixth']
        elif key == 'webglrenderingcontext.drawarrays':
            fm_keys = ['webglrenderingcontext.drawarrays-First',
            'webglrenderingcontext.drawarrays-Second',
            'webglrenderingcontext.drawarrays-Third']
        elif key == 'webgl2renderingcontext.drawarrays':
            fm_keys = ['webgl2renderingcontext.drawarrays-First',
            'webgl2renderingcontext.drawarrays-Second',
            'webgl2renderingcontext.drawarrays-Third']
        elif key == 'webglrenderingcontext.clearcolor':
            fm_keys = ['webglrenderingcontext.clearcolor-First',
            'webglrenderingcontext.clearcolor-Second',
            'webglrenderingcontext.clearcolor-Third',
            'webglrenderingcontext.clearcolor-Fourth']
        elif key == 'webgl2renderingcontext.clearcolor':
            fm_keys = ['webgl2renderingcontext.clearcolor-First',
            'webgl2renderingcontext.clearcolor-Second',
            'webgl2renderingcontext.clearcolor-Third',
            'webgl2renderingcontext.clearcolor-Fourth']
        elif key == 'webglrenderingcontext.colormask':
            fm_keys = ['webglrenderingcontext.colormask-First',
            'webglrenderingcontext.colormask-Second',
            'webglrenderingcontext.colormask-Third',
            'webglrenderingcontext.colormask-Fourth']
        elif key == 'webglrenderingcontext.getshaderprecisionformat':
            fm_keys = ['webglrenderingcontext.getshaderprecisionformat-First',
            'webglrenderingcontext.getshaderprecisionformat-Second']
        elif key == 'webgl2renderingcontext.getshaderprecisionformat':
            fm_keys = ['webgl2renderingcontext.getshaderprecisionformat-First',
            'webgl2renderingcontext.getshaderprecisionformat-Second']
        elif key == 'webglrenderingcontext.texparameteri':
            fm_keys = ['webglrenderingcontext.texparameteri-First',
            'webglrenderingcontext.texparameteri-Second',
            'webglrenderingcontext.texparameteri-Third']
        elif key == 'webgl2renderingcontext.texparameteri':
            fm_keys = ['webgl2renderingcontext.texparameteri-First',
            'webgl2renderingcontext.texparameteri-Second',
            'webgl2renderingcontext.texparameteri-Third']
        elif key == 'webglrenderingcontext.pixelstorei':
            fm_keys = ['webglrenderingcontext.pixelstorei-First',
            'webglrenderingcontext.pixelstorei-Second']
        elif key == 'webgl2renderingcontext.pixelstorei':
            fm_keys = ['webgl2renderingcontext.pixelstorei-First',
            'webgl2renderingcontext.pixelstorei-Second']
        elif key == 'webglrenderingcontext.drawelements':
            fm_keys = ['webglrenderingcontext.drawelements-First',
            'webglrenderingcontext.drawelements-Second',
            'webglrenderingcontext.drawelements-Third',
            'webglrenderingcontext.drawelements-Fourth']
        elif key == 'webgl2renderingcontext.drawelements':
            fm_keys = ['webgl2renderingcontext.drawelements-First',
            'webgl2renderingcontext.drawelements-Second',
            'webgl2renderingcontext.drawelements-Third',
            'webgl2renderingcontext.drawelements-Fourth']
        elif key == 'webglrenderingcontext.blendfunc':
            fm_keys = ['webglrenderingcontext.blendfunc-First',
            'webglrenderingcontext.blendfunc-Second']
        elif key == 'webglrenderingcontext.framebuffertexture2d':
            fm_keys = ['webglrenderingcontext.framebuffertexture2d-First',
            'webglrenderingcontext.framebuffertexture2d-Second',
            'webglrenderingcontext.framebuffertexture2d-Third']
        elif key == 'webgl2renderingcontext.framebuffertexture2d':
            fm_keys = ['webgl2renderingcontext.framebuffertexture2d-First',
            'webgl2renderingcontext.framebuffertexture2d-Second',
            'webgl2renderingcontext.framebuffertexture2d-Third']
        elif key == 'webglrenderingcontext.blendcolor':
            fm_keys = ['webglrenderingcontext.blendcolor-First',
            'webglrenderingcontext.blendcolor-Second',
            'webglrenderingcontext.blendcolor-Third',
            'webglrenderingcontext.blendcolor-Fourth']
        elif key == 'webglrenderingcontext.blendfuncseparate':
            fm_keys = ['webglrenderingcontext.blendfuncseparate-First',
            'webglrenderingcontext.blendfuncseparate-Second',
            'webglrenderingcontext.blendfuncseparate-Third',
            'webglrenderingcontext.blendfuncseparate-Fourth']
        elif key == 'webglrenderingcontext.renderbufferstorage':
            fm_keys = ['webglrenderingcontext.renderbufferstorage-First',
            'webglrenderingcontext.renderbufferstorage-Second',
            'webglrenderingcontext.renderbufferstorage-Size']
        elif key == 'webglrenderingcontext.framebufferrenderbuffer':
            fm_keys = ['webglrenderingcontext.framebufferrenderbuffer-First',
            'webglrenderingcontext.framebufferrenderbuffer-Second',
            'webglrenderingcontext.framebufferrenderbuffer-Third']
        elif key == 'webglrenderingcontext.blendequationseparate':
            fm_keys = ['webglrenderingcontext.blendequationseparate-First',
            'webglrenderingcontext.blendequationseparate-Second']   
        elif key == 'webgl2renderingcontext.blendfunc-Second':
            fm_keys = ['webgl2renderingcontext.blendfunc-First',
            'webgl2renderingcontext.blendfunc-Second']
        elif key == 'webgl2renderingcontext.viewport':
            fm_keys = ['webgl2renderingcontext.viewport-OnScreen',
            'webgl2renderingcontext.viewport-Size']
        elif key == 'webglrenderingcontext.viewport':
            fm_keys = ['webglrenderingcontext.viewport-OnScreen',
            'webglrenderingcontext.viewport-Size']
        elif key == 'webglrenderingcontext.scissor':
            fm_keys = ['webglrenderingcontext.scissor-OnScreen',
            'webglrenderingcontext.scissor-Size']
        elif key == 'webglrenderingcontext.hint':
            fm_keys = ['webglrenderingcontext.hint-First',
            'webglrenderingcontext.hint-Second']
        elif key == 'webglrenderingcontext.stencilop':
            fm_keys = ['webglrenderingcontext.stencilop-First',
            'webglrenderingcontext.stencilop-Second',
            'webglrenderingcontext.stencilop-Third']
        elif key == 'webgl2renderingcontext.stencilop':
            fm_keys = ['webgl2renderingcontext.stencilop-First',
            'webgl2renderingcontext.stencilop-Second',
            'webgl2renderingcontext.stencilop-Third']
        elif key == 'webglrenderingcontext.readpixels':
            fm_keys =['webglrenderingcontext.readpixels-OnScreen',
            'webglrenderingcontext.readpixels-Size']
        elif key == 'webgl2renderingcontext.readpixels':
            fm_keys =['webgl2renderingcontext.readpixels-OnScreen',
            'webgl2renderingcontext.readpixels-Size']
        elif key == 'webgl2renderingcontext.teximage2d':
            fm_keys = ['webgl2renderingcontext.teximage2d-First',
            'webgl2renderingcontext.teximage2d-Second',
            'webgl2renderingcontext.teximage2d-Third']
        elif key == 'webglrenderingcontext.teximage2d':
            fm_keys = ['webglrenderingcontext.teximage2d-First',
            'webglrenderingcontext.teximage2d-Second',
            'webglrenderingcontext.teximage2d-Third']
        elif key == 'webgl2renderingcontext.bufferdata':
            fm_keys = ['webgl2renderingcontext.bufferdata-First',
            'webgl2renderingcontext.bufferdata-SecondLength',
            'webgl2renderingcontext.bufferdata-Third']
        else:
            fm_keys = [key]

        if global_symbols_count[key] == 1:
            for local_key in fm_keys:
                if local_key in feature_mapping:
                    feature_header.append(feature_mapping[local_key])
        elif global_symbols_count[key] > 1 and global_symbols_count[key] < 6:
            for local_key in fm_keys:
                if local_key in feature_mapping:
                    fm_key = feature_mapping[local_key]
                    for i in range(global_symbols_count[key]):
                        feature_header.append(fm_key + '_' + str(i+1))
        elif global_symbols_count[key] > 5:
            for local_key in fm_keys:
                if local_key in feature_mapping:
                    fm_key = feature_mapping[local_key]
                    for i in range(5):
                        feature_header.append(fm_key + '_' + str(i+1))
    
    return feature_header, one_gram_header

def construct_features(data_directory, feature_mapping, global_symbols_count, url_index_mapping, features_csv):
    fd = feature_dictionaries.FeatureDictionaries()
    all_files = utilities.get_files_in_a_directory(data_directory)
    csv_header, one_gram_sequence = create_header(global_symbols_count, feature_mapping) # don't have one_gram_sequence 
    # Check if csv_header match with the one we have. # checked. It is same

    # df_labels = utilities.read_dataframe_from_json(class_labels)

    utilities.append_file(features_csv, 'hash,url_id,' + ','.join(csv_header) + ',class')

    pbar = tqdm(total=len(all_files))
    
    processed_hashes = set()
    processed_urls = set()
    # a data structure for holding urls
    processed_urls_list = []
    one_grams = {}
    temp_count = 0
    positive_counter = 0
    url_positive_counter = 0
    for f_item in all_files:
        if 'javascript_with_hash_partition' not in f_item:
            pbar.update(1)
            continue
        
        json_data = utilities.read_json(f_item)
        for key in json_data:
            add_one_grams(one_grams, global_symbols_count)
            current_features_dict = {}
            key_information = json_data[key]['information']
            script_hash = json_data[key]['content_hash']
            script_url = json_data[key]['script_url']
            
            # Because we should only keep unique scripts
            # Some instances do not have hashes but we still want to keep them
            if check_presence(processed_hashes, processed_urls, processed_urls_list, script_hash, script_url):
                continue

            # Now processing API calls per script
            for item in key_information:
                symbol_text = item['symbol'].strip().lower()

                # Update one grams
                # instead of simply keeping presence of APIs, keep a count instead. 
                if symbol_text in one_grams:
                    one_grams[symbol_text] = one_grams[symbol_text] + 1       
                
                # Here we extract values and arguments for symbols and build a dictionary

                if item['value'] is not None and item['value'] != 'null' and item['value'].strip() != '':
                    if symbol_text in fd.value_numeric_features:
                        symbol_encoding = feature_mapping[symbol_text]
                        if symbol_encoding not in current_features_dict:
                            current_features_dict[symbol_encoding] = []

                        if len(current_features_dict[symbol_encoding]) < 6:
                            if utilities.isint(item['value']) or utilities.isfloat(item['value']):
                                current_features_dict[symbol_encoding].append(item['value'])
                            else: # should never occur
                                print('(' + symbol_text + ') not a number (value): ' + item['value'])
                        
                    elif symbol_text in fd.value_categorical_features:
                        symbol_encoding = feature_mapping[symbol_text]
                        if symbol_encoding not in current_features_dict:
                            current_features_dict[symbol_encoding] = []

                        if len(current_features_dict[symbol_encoding]) < 6:
                            current_features_dict[symbol_encoding].append(item['value'])

                    elif symbol_text in fd.value_length_features:
                        symbol_encoding = feature_mapping[symbol_text]
                        if symbol_encoding not in current_features_dict:
                            current_features_dict[symbol_encoding] = []

                        if len(current_features_dict[symbol_encoding]) < 6:
                            current_features_dict[symbol_encoding].append(len(item['value']))

                    elif symbol_text in fd.value_json_length_features:
                        symbol_encoding = feature_mapping[symbol_text]
                        if symbol_encoding not in current_features_dict:
                            current_features_dict[symbol_encoding] = []

                        if len(current_features_dict[symbol_encoding]) < 6:
                            try:
                                current_features_dict[symbol_encoding].append(len(json.loads(item['value'])))
                            except Exception as e:
                                print('[line 199]', item['value'])

                    elif symbol_text == 'window.document.cookie':
                        symbol_encoding = feature_mapping[symbol_text]
                        if symbol_encoding not in current_features_dict:
                            current_features_dict[symbol_encoding] = []

                        if len(current_features_dict[symbol_encoding]) < 6:           
                            current_features_dict[symbol_encoding].append(len(item['value'].split(';')))
                    
                    elif symbol_text == 'canvasrenderingcontext2d.strokestyle' or \
                            symbol_text == 'canvasrenderingcontext2d.fillstyle' or \
                            symbol_text == 'canvasrenderingcontext2d.shadowcolor':
                        symbol_encoding = feature_mapping[symbol_text]
                        if symbol_encoding not in current_features_dict:
                            current_features_dict[symbol_encoding] = []

                        if len(current_features_dict[symbol_encoding]) < 6:
                            if '(' in item['value']:                
                                current_features_dict[symbol_encoding].append('gradient')
                            else:
                                current_features_dict[symbol_encoding].append('color')
                    
                    elif symbol_text == 'canvasrenderingcontext2d.filter':
                        symbol_encoding = feature_mapping[symbol_text]
                        if symbol_encoding not in current_features_dict:
                            current_features_dict[symbol_encoding] = []

                        if len(current_features_dict[symbol_encoding]) < 6:
                            if '(' in item['value']:                
                                current_features_dict[symbol_encoding].append(item['value'].split('(')[0])
                            else:
                                current_features_dict[symbol_encoding].append('')
                
                elif item['argument'] is not None and item['argument'] != 'null' and item['argument'].strip() != '':
                    if symbol_text in fd.arguments_numeric_features:
                        symbol_encoding = feature_mapping[symbol_text]
                        if symbol_encoding not in current_features_dict:
                            current_features_dict[symbol_encoding] = []
                    
                        if len(current_features_dict[symbol_encoding]) < 6:
                            if utilities.isint(item['argument']) or utilities.isfloat(item['argument']):
                                current_features_dict[symbol_encoding].append(item['argument'])
                            else: # should never occur
                                print('(' + symbol_text + ')not a number (argument):' + item['argument'])

                    elif symbol_text in fd.arguments_categorical_features:
                        symbol_encoding = feature_mapping[symbol_text]
                        f_args = json.loads(item['argument'])

                        if symbol_encoding not in current_features_dict:
                            current_features_dict[symbol_encoding] = []
                        
                        if len(current_features_dict[symbol_encoding]) < 6:
                            if f_args['0'] is not None:
                                current_features_dict[symbol_encoding].append(f_args['0'])
            
                    elif symbol_text in fd.arguments_length_features:
                        symbol_encoding = feature_mapping[symbol_text]
                        if symbol_encoding not in current_features_dict:
                            current_features_dict[symbol_encoding] = []
                        
                        if len(current_features_dict[symbol_encoding]) < 6:
                            current_features_dict[symbol_encoding].append(len(item['argument']))

                    elif symbol_text in fd.argument_json_length_features:
                        symbol_encoding = feature_mapping[symbol_text]
                        if symbol_encoding not in current_features_dict:
                            current_features_dict[symbol_encoding] = []
                        
                        if len(current_features_dict[symbol_encoding]) < 6:
                            try:          
                                current_features_dict[symbol_encoding].append(len(json.loads(item['argument'])))
                            except Exception as e:
                                print('[line 314]', item['argument'])

                    elif symbol_text == 'canvasrenderingcontext2d.fillrect' or \
                        symbol_text == 'canvasrenderingcontext2d.rect' or \
                        symbol_text == 'canvasrenderingcontext2d.arc' or \
                        symbol_text == 'canvasrenderingcontext2d.getimagedata' or \
                        symbol_text == 'canvasrenderingcontext2d.strokerect' or \
                        symbol_text == 'canvasrenderingcontext2d.clearrect' or \
                        symbol_text == 'webgl2renderingcontext.viewport' or \
                        symbol_text == 'webglrenderingcontext.viewport' or \
                        symbol_text == 'webglrenderingcontext.scissor' or \
                        symbol_text == 'webgl2renderingcontext.readpixels' or \
                        symbol_text == 'webglrenderingcontext.readpixels':
                        feature_encoding_OnScreen = feature_mapping[symbol_text + '-OnScreen']
                        feature_encoding_Size = feature_mapping[symbol_text + '-Size']
                         
                        f_args = json.loads(item['argument'])
                        if feature_encoding_OnScreen not in current_features_dict:
                            current_features_dict[feature_encoding_OnScreen] = []
                        
                        if len(current_features_dict[feature_encoding_OnScreen]) < 6:
                            
                            if (f_args['0'] is not None and f_args['1'] is not None) and (utilities.isint(f_args['0']) or utilities.isfloat(f_args['0'])) and \
                                 (utilities.isint(f_args['1']) or utilities.isfloat(f_args['1'])):
                                if float(f_args['0']) >= 0 and float(f_args['1']) >= 0:
                                    current_features_dict[feature_encoding_OnScreen].append(1)
                                else:
                                    current_features_dict[feature_encoding_OnScreen].append(0)
                            else:
                                current_features_dict[feature_encoding_OnScreen].append(0)


                        if feature_encoding_Size not in current_features_dict:
                            current_features_dict[feature_encoding_Size] = []
                        
                        if len(current_features_dict[feature_encoding_Size]) < 6:
                            if symbol_text == 'canvasrenderingcontext2d.arc':
                                if f_args['2'] is not None:
                                    current_features_dict[feature_encoding_Size].append((3.1415) * (float(f_args['2']) * float(f_args['2'])))
                                else:
                                    current_features_dict[feature_encoding_Size].append(0)
                            else:
                                if f_args['2'] is not None and f_args['3'] is not None:
                                    if utilities.isfloat(f_args['2']) and utilities.isfloat(f_args['3']):
                                        current_features_dict[feature_encoding_Size].append(float(f_args['2']) * float(f_args['3']))
                                    else:
                                        current_features_dict[feature_encoding_Size].append(0)
                                else:
                                    current_features_dict[feature_encoding_Size].append(0)
                
                    elif symbol_text == 'canvasrenderingcontext2d.createradialgradient':
                        feature_encoding_OnScreen_One = feature_mapping[symbol_text + '-OnScreen-One']
                        feature_encoding_OnScreen_Two = feature_mapping[symbol_text + '-OnScreen-Two']
                        feature_encoding_Size_One = feature_mapping[symbol_text + '-Size-One']
                        feature_encoding_Size_Two = feature_mapping[symbol_text + '-Size-Two']

                        f_args = json.loads(item['argument'])

                        if feature_encoding_OnScreen_One not in current_features_dict:
                            current_features_dict[feature_encoding_OnScreen_One] = []
                        
                        if len(current_features_dict[feature_encoding_OnScreen_One]) < 6:
                            if (f_args['0'] is not None and f_args['1'] is not None) and (f_args['0'] >= 0 and f_args['1'] >= 0):
                                current_features_dict[feature_encoding_OnScreen_One].append(1)
                            else:
                                current_features_dict[feature_encoding_OnScreen_One].append(0)
                        
                        if feature_encoding_OnScreen_Two not in current_features_dict:
                            current_features_dict[feature_encoding_OnScreen_Two] = []
                        
                        if len(current_features_dict[feature_encoding_OnScreen_Two]) < 6:
                            if  (f_args['3'] is not None and f_args['4'] is not None) and (f_args['3'] >= 0 and f_args['4'] >= 0):
                                current_features_dict[feature_encoding_OnScreen_Two].append(1)
                            else:
                                current_features_dict[feature_encoding_OnScreen_Two].append(0)
                        
                        if feature_encoding_Size_One not in current_features_dict:
                            current_features_dict[feature_encoding_Size_One] = []
                        
                        if len(current_features_dict[feature_encoding_Size_One]) < 6:
                            if f_args['2'] is not None:
                                current_features_dict[feature_encoding_Size_One].append((3.1415) * (float(f_args['2']) * float(f_args['2'])))
                            else:
                                current_features_dict[feature_encoding_Size_One].append(0)

                        if feature_encoding_Size_Two not in current_features_dict:
                            current_features_dict[feature_encoding_Size_Two] = []
                        
                        if len(current_features_dict[feature_encoding_Size_Two]) < 6:
                            if f_args['5'] is not None:
                                current_features_dict[feature_encoding_Size_Two].append((3.1415) * (float(f_args['5']) * float(f_args['5'])))
                            else:
                                current_features_dict[feature_encoding_Size_Two].append(0)
                  
                
                    elif symbol_text == 'canvasrenderingcontext2d.beziercurveto':
                        feature_encoding_OnScreen = feature_mapping[symbol_text + '-OnScreen']
                        feature_encoding_Size_One = feature_mapping[symbol_text + '-Size-One']
                        feature_encoding_Size_Two = feature_mapping[symbol_text + '-Size-Two']

                        f_args = json.loads(item['argument'])
                        if feature_encoding_OnScreen not in current_features_dict:
                            current_features_dict[feature_encoding_OnScreen] = []
                        
                        if len(current_features_dict[feature_encoding_OnScreen]) < 6:
                            if f_args['0'] >= 0 and f_args['1'] >= 0 and f_args['2'] >= 0 and f_args['3'] >= 0 and f_args['4'] >= 0 and f_args['5'] >= 0:
                                current_features_dict[feature_encoding_OnScreen].append(1)
                            else:
                                current_features_dict[feature_encoding_OnScreen].append(0)


                        if feature_encoding_Size_One not in current_features_dict:
                            current_features_dict[feature_encoding_Size_One] = []
                        
                        if len(current_features_dict[feature_encoding_Size_One]) < 6:
                            current_features_dict[feature_encoding_Size_One].append(math.sqrt((float(f_args['0']) - float(f_args['2']))**2 + (float(f_args['1']) - float(f_args['3']))**2))
                        
                        if feature_encoding_Size_Two not in current_features_dict:
                            current_features_dict[feature_encoding_Size_Two] = []
                        
                        if len(current_features_dict[feature_encoding_Size_Two]) < 6:
                            current_features_dict[feature_encoding_Size_Two].append(math.sqrt((float(f_args['2']) - float(f_args['4']))**2 + (float(f_args['3']) - float(f_args['5']))**2))

                    elif symbol_text == 'canvasrenderingcontext2d.filltext' or symbol_text == 'canvasrenderingcontext2d.stroketext':
                        feature_encoding_OnScreen = feature_mapping[symbol_text + '-OnScreen']
                        feature_encoding_Size = feature_mapping[symbol_text + '-TextSize']
                        
                        f_args = json.loads(item['argument'])

                        if feature_encoding_OnScreen not in current_features_dict:
                            current_features_dict[feature_encoding_OnScreen] = []
                        
                        if len(current_features_dict[feature_encoding_OnScreen]) < 6:
                            if (utilities.isint(f_args['1']) or utilities.isfloat(f_args['1'])) and (utilities.isint(f_args['2']) or utilities.isfloat(f_args['2'])):
                                if float(f_args['1']) >= 0 and float(f_args['2']) >= 0:
                                    current_features_dict[feature_encoding_OnScreen].append(1)
                                else:
                                    current_features_dict[feature_encoding_OnScreen].append(0)
                            else:
                                current_features_dict[feature_encoding_OnScreen].append(0)

                        if feature_encoding_Size not in current_features_dict:
                            current_features_dict[feature_encoding_Size] = []
                        
                        if len(current_features_dict[feature_encoding_Size]) < 6:
                            if utilities.isint(f_args['0']):
                                current_features_dict[feature_encoding_Size].append(f_args['0'])
                            else:
                                if utilities.isfloat(f_args['0']):
                                    current_features_dict[feature_encoding_Size].append(0)
                                else:
                                    current_features_dict[feature_encoding_Size].append(len(f_args['0']))
                
                    elif symbol_text == 'htmlcanvaselement.getelementsbytagname' or \
                         symbol_text == 'document.getelementsbytagname' or \
                         symbol_text == 'canvasrenderingcontext2d.createpattern' or \
                         symbol_text == 'audiocontext.createchannelmerger': 

                        feature_encoding = feature_mapping[symbol_text]

                        f_args = json.loads(item['argument'])

                        if feature_encoding not in current_features_dict:
                            current_features_dict[feature_encoding] = []
                        
                        if len(current_features_dict[feature_encoding]) < 6:
                            if symbol_text == 'canvasrenderingcontext2d.createpattern':
                                current_features_dict[feature_encoding].append(f_args['1'])
                            else:
                                current_features_dict[feature_encoding].append(f_args['0'])
                
                    elif symbol_text == 'canvasrenderingcontext2d.createlineargradient':
                        feature_encoding = feature_mapping[symbol_text]
                        f_args = json.loads(item['argument'])
                        
                        if feature_encoding not in current_features_dict:
                            current_features_dict[feature_encoding] = []
                        
                        if len(current_features_dict[feature_encoding]) < 6:
                            current_features_dict[feature_encoding].append(math.sqrt((float(f_args['0']) - float(f_args['2']))**2 + (float(f_args['1']) - float(f_args['3']))**2))

                    elif symbol_text == 'canvasrenderingcontext2d.putimagedata':
                        feature_encoding = feature_mapping[symbol_text]

                        f_args = json.loads(item['argument'])

                        if feature_encoding not in current_features_dict:
                            current_features_dict[feature_encoding] = []
                        
                        if len(current_features_dict[feature_encoding]) < 6:
                            if float(f_args['1']) >= 0 and float(f_args['2']) >= 0:
                                current_features_dict[feature_encoding].append(1)
                            else:
                                current_features_dict[feature_encoding].append(0)

                
                    elif symbol_text == 'canvasrenderingcontext2d.setlinedash':
                        feature_encoding = feature_mapping[symbol_text]

                        if feature_encoding not in current_features_dict:
                            current_features_dict[feature_encoding] = []
                        
                        if len(current_features_dict[feature_encoding]) < 6:
                            try:
                                f_args = json.loads(item['argument'])
                                current_features_dict[feature_encoding].append(len(f_args['0']))
                            except Exception as e:
                                current_features_dict[feature_encoding].append(0)
                                print('[line 429]', item['argument'])

                    elif symbol_text == 'canvasrenderingcontext2d.createimagedata':
                        feature_encoding = feature_mapping[symbol_text]
                                             
                        f_args = json.loads(item['argument'])

                        if feature_encoding not in current_features_dict:
                            current_features_dict[feature_encoding] = []
                        
                        if len(current_features_dict[feature_encoding]) < 6:
                            if '0' in f_args and '1' in f_args:
                                if (f_args['0'] is not None and f_args['1'] is not None) and (utilities.isfloat(f_args['0']) and utilities.isfloat(f_args['1'])):
                                    current_features_dict[feature_encoding].append(float(f_args['0']) * float(f_args['1']))
                                else:
                                    current_features_dict[feature_encoding].append(0)
                            else:
                                current_features_dict[feature_encoding].append(0)
                

                    elif symbol_text == 'canvasrenderingcontext2d.arcto':
                        feature_encoding_OnScreen = feature_mapping[symbol_text + '-OnScreen']
                        feature_encoding_Size_One = feature_mapping[symbol_text + '-Size-One']
                        feature_encoding_Size_Two = feature_mapping[symbol_text + '-Size-Two']

                        f_args = json.loads(item['argument'])
                        
                        if feature_encoding_OnScreen not in current_features_dict:
                            current_features_dict[feature_encoding_OnScreen] = []
                        
                        if len(current_features_dict[feature_encoding_OnScreen]) < 6:
                            if (f_args['0'] is not None and f_args['1'] is not None and f_args['2'] is not None and f_args['3'] is not None)\
                                 and (utilities.isfloat(f_args['0']) and utilities.isfloat(f_args['1']) and utilities.isfloat(f_args['2']) and utilities.isfloat(f_args['3']))\
                                 and (float(f_args['0']) >= 0 and float(f_args['1']) >= 0 and float(f_args['2']) >= 0 and float(f_args['3']) >= 0):
                                current_features_dict[feature_encoding_OnScreen].append(1)
                            else:
                                current_features_dict[feature_encoding_OnScreen].append(0)

                        if feature_encoding_Size_One not in current_features_dict:
                            current_features_dict[feature_encoding_Size_One] = []
                        
                        if len(current_features_dict[feature_encoding_Size_One]) < 6:
                            if f_args['0'] is not None and f_args['1'] is not None and f_args['2'] is not None and f_args['3'] is not None:
                                current_features_dict[feature_encoding_Size_One].append(math.sqrt((float(f_args['0']) - float(f_args['2']))**2 + (float(f_args['1']) - float(f_args['3']))**2))
                        
                        if feature_encoding_Size_Two not in current_features_dict:
                            current_features_dict[feature_encoding_Size_Two] = []
                        
                        if len(current_features_dict[feature_encoding_Size_Two]) < 6:
                            current_features_dict[feature_encoding_Size_Two].append((3.1415) * (float(f_args['4']) * float(f_args['4'])))

                    elif symbol_text == 'audiocontext.createbuffer':                
                        feature_encoding_NumChannels = feature_mapping[symbol_text + '-NumChannels']
                        feature_encoding_Length = feature_mapping[symbol_text+ '-Length']
                        feature_encoding_SampleRate = feature_mapping[symbol_text + '-SampleRate']
                        
                        f_args = json.loads(item['argument'])

                        if feature_encoding_NumChannels not in current_features_dict:
                            current_features_dict[feature_encoding_NumChannels] = []
                        
                        if len(current_features_dict[feature_encoding_NumChannels]) < 6:
                            current_features_dict[feature_encoding_NumChannels].append(f_args['0'])
                        
                        if feature_encoding_Length not in current_features_dict:
                            current_features_dict[feature_encoding_Length] = []
                        
                        if len(current_features_dict[feature_encoding_Length]) < 6:
                            current_features_dict[feature_encoding_Length].append(f_args['1'])

                        if feature_encoding_SampleRate not in current_features_dict:
                            current_features_dict[feature_encoding_SampleRate] = []
                        
                        if len(current_features_dict[feature_encoding_SampleRate]) < 6:
                            current_features_dict[feature_encoding_SampleRate].append(f_args['2'])
                
                    elif symbol_text == 'offlineaudiocontext.createscriptprocessor' or symbol_text == 'audiocontext.createscriptprocessor':
                        feature_encoding_BufferSize = feature_mapping[symbol_text + '-BufferSize']
                        feature_encoding_InNumChannels = feature_mapping[symbol_text + '-InNumChannels']
                        feature_encoding_OutNumChannels = feature_mapping[symbol_text + '-OutNumChannels']

                        f_args = json.loads(item['argument'])

                        if feature_encoding_BufferSize not in current_features_dict:
                            current_features_dict[feature_encoding_BufferSize] = []
                        
                        if len(current_features_dict[feature_encoding_BufferSize]) < 6:
                             current_features_dict[feature_encoding_BufferSize].append(f_args['0'])
                        
                        if feature_encoding_InNumChannels not in current_features_dict:
                            current_features_dict[feature_encoding_InNumChannels] = []
                        
                        if len(current_features_dict[feature_encoding_InNumChannels]) < 6:
                            if '1' in f_args:
                                current_features_dict[feature_encoding_InNumChannels].append(f_args['1'])

                        if feature_encoding_OutNumChannels not in current_features_dict:
                            current_features_dict[feature_encoding_OutNumChannels] = []
                        
                        if len(current_features_dict[feature_encoding_OutNumChannels]) < 6:
                            if '2' in f_args:
                                current_features_dict[feature_encoding_OutNumChannels].append(f_args['2'])
                    
                    elif symbol_text == 'canvasrenderingcontext2d.moveto' or \
                        symbol_text == 'canvasrenderingcontext2d.lineto' or \
                        symbol_text == 'canvasrenderingcontext2d.translate' or \
                        symbol_text == 'canvasrenderingcontext2d.drawimage':
                        feature_encoding = feature_mapping[symbol_text]                     
                        f_args = json.loads(item['argument'])

                        if feature_encoding not in current_features_dict:
                            current_features_dict[feature_encoding] = []

                        if len(current_features_dict[feature_encoding]) < 6:
                            if symbol_text == 'canvasrenderingcontext2d.drawimage':
                                index_1 = '1'
                                index_2 = '2'
                            else:
                                index_1 = '0'
                                index_2 = '1'
                            if (f_args[index_1] is not None and f_args[index_2] is not None) and \
                                 (utilities.isint(f_args[index_1]) or utilities.isfloat(f_args[index_1])) and \
                                     (utilities.isint(f_args[index_2]) or utilities.isfloat(f_args[index_2])):
                                if float(f_args[index_1]) >= 0 and float(f_args[index_2]) >= 0:
                                    current_features_dict[feature_encoding].append(1)
                                else:
                                    current_features_dict[feature_encoding].append(0)
                            else:
                                current_features_dict[feature_encoding].append(0)

                    elif symbol_text == 'canvasrenderingcontext2d.quadraticcurveto':
                        feature_encoding_OnScreen = feature_mapping[symbol_text + '-OnScreen']
                        feature_encoding_Size = feature_mapping[symbol_text + '-Size']

                        f_args = json.loads(item['argument'])
                        if feature_encoding_OnScreen not in current_features_dict:
                            current_features_dict[feature_encoding_OnScreen] = []
                        
                        if len(current_features_dict[feature_encoding_OnScreen]) < 6:
                            if (f_args['0'] is not None and f_args['1'] is not None and f_args['2'] is not None and f_args['3'] is not None)\
                                and (utilities.isfloat(f_args['0']) and utilities.isfloat(f_args['1']) and utilities.isfloat(f_args['2']) and utilities.isfloat(f_args['3']))\
                                 and (float(f_args['0']) >= 0 and float(f_args['1']) >= 0 and float(f_args['2']) >= 0 and float(f_args['3']) >= 0):
                                current_features_dict[feature_encoding_OnScreen].append(1)
                            else:
                                current_features_dict[feature_encoding_OnScreen].append(0)


                        if feature_encoding_Size not in current_features_dict:
                            current_features_dict[feature_encoding_Size] = []
                        
                        if len(current_features_dict[feature_encoding_Size]) < 6:
                            current_features_dict[feature_encoding_Size].append(math.sqrt((float(f_args['0']) - float(f_args['2']))**2 + (float(f_args['1']) - float(f_args['3']))**2))

                    elif symbol_text == 'webglrenderingcontext.bufferdata':
                        symbol_encoding_First = feature_mapping[symbol_text + '-First']
                        symbol_encoding_Last = feature_mapping[symbol_text + '-Last']
                        
                        f_args = json.loads(item['argument'])

                        if symbol_encoding_First not in current_features_dict:
                            current_features_dict[symbol_encoding_First] = []
                        
                        if len(current_features_dict[symbol_encoding_First]) < 6:
                            if f_args['0'] is not None:
                                current_features_dict[symbol_encoding_First].append(f_args['0'])
                        
                        if symbol_encoding_Last not in current_features_dict:
                            current_features_dict[symbol_encoding_Last] = []
                        
                        if len(current_features_dict[symbol_encoding_Last]) < 6:
                            if f_args['2'] is not None:
                                current_features_dict[symbol_encoding_Last].append(f_args['2'])
                    
                    elif symbol_text == 'webglrenderingcontext.getattriblocation' or \
                        symbol_text == 'webgl2renderingcontext.getattriblocation' or \
                        symbol_text == 'webglrenderingcontext.getuniformlocation' or \
                        symbol_text == 'webgl2renderingcontext.getuniformlocation' or \
                        symbol_text == 'webglrenderingcontext.getshaderparameter' or \
                        symbol_text == 'webglrenderingcontext.getprogramparameter' or \
                        symbol_text == 'webglrenderingcontext.getactiveattrib' or \
                        symbol_text == 'webglrenderingcontext.getactiveuniform' or \
                        symbol_text == 'webgl2renderingcontext.getshaderparameter' or \
                        symbol_text == 'webgl2renderingcontext.getprogramparameter' or \
                        symbol_text == 'webgl2renderingcontext.getactiveattrib' or \
                        symbol_text == 'webgl2renderingcontext.getactiveuniform' or \
                        symbol_text == 'webglrenderingcontext.bindattriblocation':
                        symbol_encoding = feature_mapping[symbol_text]
                        f_args = json.loads(item['argument'])

                        if symbol_encoding not in current_features_dict:
                            current_features_dict[symbol_encoding] = []
                        
                        if len(current_features_dict[symbol_encoding]) < 6:
                            if f_args['1'] is not None:
                                current_features_dict[symbol_encoding].append(f_args['1'])
                    
                    elif symbol_text == 'webglrenderingcontext.uniform2f' or \
                        symbol_text == 'webgl2renderingcontext.uniform2f':
                        symbol_encoding_Second = feature_mapping[symbol_text + '-Second']
                        symbol_encoding_Third = feature_mapping[symbol_text + '-Third']
                        
                        f_args = json.loads(item['argument'])

                        if symbol_encoding_Second not in current_features_dict:
                            current_features_dict[symbol_encoding_Second] = []
                        
                        if len(current_features_dict[symbol_encoding_Second]) < 6:
                            if f_args['1'] is not None:
                                current_features_dict[symbol_encoding_Second].append(f_args['1'])
                        
                        if symbol_encoding_Third not in current_features_dict:
                            current_features_dict[symbol_encoding_Third] = []
                        
                        if len(current_features_dict[symbol_encoding_Third]) < 6:
                            if f_args['2'] is not None:
                                current_features_dict[symbol_encoding_Third].append(f_args['2'])
                    
                    elif symbol_text == 'webglrenderingcontext.vertexattribpointer' or \
                        symbol_text == 'webgl2renderingcontext.vertexattribpointer' or \
                        symbol_text == 'webglrenderingcontext.drawarrays' or \
                        symbol_text == 'webgl2renderingcontext.drawarrays' or \
                        symbol_text == 'webglrenderingcontext.clearcolor' or \
                        symbol_text == 'webgl2renderingcontext.clearcolor' or \
                        symbol_text == 'webglrenderingcontext.getshaderprecisionformat' or \
                        symbol_text == 'webgl2renderingcontext.getshaderprecisionformat' or \
                        symbol_text == 'webglrenderingcontext.texparameteri' or \
                        symbol_text == 'webgl2renderingcontext.texparameteri' or \
                        symbol_text == 'webglrenderingcontext.pixelstorei' or \
                        symbol_text == 'webgl2renderingcontext.pixelstorei' or \
                        symbol_text == 'webglrenderingcontext.drawelements' or \
                        symbol_text == 'webgl2renderingcontext.drawelements' or \
                        symbol_text == 'webglrenderingcontext.blendfunc' or \
                        symbol_text == 'webglrenderingcontext.framebuffertexture2d' or \
                        symbol_text == 'webgl2renderingcontext.framebuffertexture2d' or \
                        symbol_text == 'webgl2renderingcontext.teximage2d' or \
                        symbol_text == 'webglrenderingcontext.teximage2d' or \
                        symbol_text == 'webglrenderingcontext.blendcolor' or \
                        symbol_text == 'webglrenderingcontext.colormask' or \
                        symbol_text == 'webglrenderingcontext.blendfuncseparate' or \
                        symbol_text == 'webglrenderingcontext.framebufferrenderbuffer' or \
                        symbol_text == 'webglrenderingcontext.blendequationseparate' or \
                        symbol_text == 'webgl2renderingcontext.blendfunc' or \
                        symbol_text == 'webglrenderingcontext.hint' or \
                        symbol_text == 'webglrenderingcontext.stencilop' or \
                        symbol_text == 'webgl2renderingcontext.stencilop':

                        symbol_encoding_First = feature_mapping[symbol_text + '-First']
                        symbol_encoding_Second = feature_mapping[symbol_text + '-Second']

                        f_args = json.loads(item['argument'])

                        if symbol_encoding_First not in current_features_dict:
                            current_features_dict[symbol_encoding_First] = []
                        
                        if len(current_features_dict[symbol_encoding_First]) < 6:
                            if f_args['0'] is not None:
                                current_features_dict[symbol_encoding_First].append(f_args['0'])
                        
                        if symbol_encoding_Second not in current_features_dict:
                            current_features_dict[symbol_encoding_Second] = []
                        
                        if len(current_features_dict[symbol_encoding_Second]) < 6:
                            if f_args['1'] is not None:
                                current_features_dict[symbol_encoding_Second].append(f_args['1'])
                        
                        if symbol_text == 'webglrenderingcontext.vertexattribpointer' or \
                            symbol_text == 'webgl2renderingcontext.vertexattribpointer' or \
                            symbol_text == 'webglrenderingcontext.clearcolor' or \
                            symbol_text == 'webgl2renderingcontext.clearcolor' or \
                            symbol_text == 'webglrenderingcontext.drawarrays' or \
                            symbol_text == 'webgl2renderingcontext.drawarrays' or \
                            symbol_text == 'webglrenderingcontext.texparameteri' or \
                            symbol_text == 'webgl2renderingcontext.texparameteri' or \
                            symbol_text == 'webglrenderingcontext.drawelements' or \
                            symbol_text == 'webgl2renderingcontext.drawelements' or \
                            symbol_text == 'webglrenderingcontext.framebuffertexture2d' or \
                            symbol_text == 'webgl2renderingcontext.framebuffertexture2d' or \
                            symbol_text == 'webgl2renderingcontext.teximage2d' or \
                            symbol_text == 'webglrenderingcontext.teximage2d' or \
                            symbol_text == 'webglrenderingcontext.blendcolor' or \
                            symbol_text == 'webglrenderingcontext.colormask' or \
                            symbol_text == 'webglrenderingcontext.blendfuncseparate' or \
                            symbol_text == 'webglrenderingcontext.framebufferrenderbuffer' or \
                            symbol_text == 'webglrenderingcontext.stencilop' or \
                            symbol_text == 'webgl2renderingcontext.stencilop':

                            symbol_encoding_Third = feature_mapping[symbol_text + '-Third']
                            if symbol_encoding_Third not in current_features_dict:
                                current_features_dict[symbol_encoding_Third] = []
                            
                            if len(current_features_dict[symbol_encoding_Third]) < 6:
                                if f_args['2'] is not None:
                                    current_features_dict[symbol_encoding_Third].append(f_args['2'])

                        if symbol_text == 'webglrenderingcontext.vertexattribpointer' or \
                            symbol_text == 'webgl2renderingcontext.vertexattribpointer' or \
                            symbol_text == 'webglrenderingcontext.clearcolor' or \
                            symbol_text == 'webgl2renderingcontext.clearcolor' or \
                            symbol_text == 'webglrenderingcontext.drawelements' or \
                            symbol_text == 'webgl2renderingcontext.drawelements' or \
                            symbol_text == 'webglrenderingcontext.blendcolor' or \
                            symbol_text == 'webglrenderingcontext.colormask' or \
                            symbol_text == 'webglrenderingcontext.blendfuncseparate':
                            symbol_encoding_Fourth = feature_mapping[symbol_text + '-Fourth']
                            if symbol_encoding_Fourth not in current_features_dict:
                                current_features_dict[symbol_encoding_Fourth] = []
                            
                            if len(current_features_dict[symbol_encoding_Fourth]) < 6:
                                if f_args['3'] is not None:
                                    current_features_dict[symbol_encoding_Fourth].append(f_args['3'])
                            
                        if symbol_text == 'webglrenderingcontext.vertexattribpointer' or \
                            symbol_text == 'webgl2renderingcontext.vertexattribpointer':
                            symbol_encoding_Fifth = feature_mapping[symbol_text + '-Fifth']
                            symbol_encoding_Sixth = feature_mapping[symbol_text + '-Sixth']
                            
                            if symbol_encoding_Fifth not in current_features_dict:
                                current_features_dict[symbol_encoding_Fifth] = []

                            if len(current_features_dict[symbol_encoding_Fifth]) < 6:
                                if f_args['4'] is not None:
                                    current_features_dict[symbol_encoding_Fifth].append(f_args['4'])
                            
                            if symbol_encoding_Sixth not in current_features_dict:
                                current_features_dict[symbol_encoding_Sixth] = []
                            
                            if len(current_features_dict[symbol_encoding_Sixth]) < 6:
                                if f_args['5'] is not None:
                                    current_features_dict[symbol_encoding_Sixth].append(f_args['5'])
                    
                    elif symbol_text == 'webglrenderingcontext.renderbufferstorage':
                        symbol_encoding_First = feature_mapping[symbol_text + '-First']
                        symbol_encoding_Second = feature_mapping[symbol_text + '-Second']
                        symbol_encoding_Size = feature_mapping[symbol_text + '-Size']
                        
                        f_args = json.loads(item['argument'])

                        if symbol_encoding_First not in current_features_dict:
                            current_features_dict[symbol_encoding_First] = []
                        
                        if len(current_features_dict[symbol_encoding_First]) < 6:
                            if f_args['0'] is not None:
                                current_features_dict[symbol_encoding_First].append(f_args['0'])
                        
                        if symbol_encoding_Second not in current_features_dict:
                            current_features_dict[symbol_encoding_Second] = []
                        
                        if len(current_features_dict[symbol_encoding_Second]) < 6:
                            if f_args['1'] is not None:
                                current_features_dict[symbol_encoding_Second].append(f_args['1'])
                        
                        if symbol_encoding_Size not in current_features_dict:
                            current_features_dict[symbol_encoding_Size] = []
                        
                        if len(current_features_dict[symbol_encoding_Size]) < 6:
                            current_features_dict[symbol_encoding_Size].append(float(f_args['2']) * float(f_args['3']))
                    
                    elif symbol_text == 'webgl2renderingcontext.bufferdata':
                        symbol_encoding_First = feature_mapping[symbol_text + '-First']
                        symbol_encoding_Second = feature_mapping[symbol_text + '-SecondLength']
                        symbol_encoding_Size = feature_mapping[symbol_text + '-Third']
                        
                        f_args = json.loads(item['argument'])

                        if symbol_encoding_First not in current_features_dict:
                            current_features_dict[symbol_encoding_First] = []
                        
                        if len(current_features_dict[symbol_encoding_First]) < 6:
                            if f_args['0'] is not None:
                                current_features_dict[symbol_encoding_First].append(f_args['0'])
                        
                        if symbol_encoding_Second not in current_features_dict:
                            current_features_dict[symbol_encoding_Second] = []
                        
                        if len(current_features_dict[symbol_encoding_Second]) < 6:
                            if f_args['1'] is not None and not utilities.isfloat(f_args['1']):
                                current_features_dict[symbol_encoding_Second].append(len(f_args['1']))
                            else:
                                current_features_dict[symbol_encoding_Second].append(0)
                        
                        if symbol_encoding_Size not in current_features_dict:
                            current_features_dict[symbol_encoding_Size] = []
                        
                        if len(current_features_dict[symbol_encoding_Size]) < 6:
                            current_features_dict[symbol_encoding_Size].append(f_args['2'])



            # Start writing the script vector here.
            # argument_json_numeric_features not handled at the moment. Take care of it.
            row_to_add = []
            for item in csv_header:
                if item.startswith('fog'):
                    row_to_add.append(one_grams[one_gram_sequence[int(item.split('fog')[1])]])
                elif '_' in item:
                    index = int(item.split('_')[1])
                    if item.split('_')[0] not in current_features_dict:
                        # if the value is not present treat it as empty
                        row_to_add.append('')
                    else:
                        current_item = current_features_dict[item.split('_')[0]]
                        if index <= len(current_item):
                            row_to_add.append(current_item[index - 1])
                        if index > len(current_item):
                            # if the value is not present treat it as empty
                            row_to_add.append('')
                else:
                    if item not in current_features_dict:
                        # if the value is not present treat it as empty
                        row_to_add.append('')
                    else:
                        row_to_add.append(current_features_dict[item])
            try:
                url_index = str(processed_urls_list.index(script_url))
            except ValueError:
                url_index = 'N'
            
            label = '?'
            # if script_hash != '':
            #     if df_labels['content_hash'].str.contains(script_hash, na=False, regex=False).any():
            #         label = '?'
            #         positive_counter += 1
            # elif script_url != '':
            #     if df_labels['script_url'].str.contains(script_url, na=False, regex=False).any():
            #         label = '?'
            #         url_positive_counter += 1

            feature_str = script_hash + ',' + 'URL_' + url_index + ',' + ','.join(str(i).replace(',', '') for i in row_to_add) + ',' + label
            utilities.append_file(features_csv,feature_str)
            
            temp_count += 1
            if temp_count % 10000 == 0:
                print('Total Processed: , Total Positives (hash, url)', temp_count, positive_counter, url_positive_counter)

        pbar.update(1)
        # for now, remove it when we are removing break
        # utilities.write_list_simple(url_index_mapping, processed_urls_list)
        # break
    utilities.write_list_simple(url_index_mapping, processed_urls_list)
    return 

def remove_unwanted_characters_from_csv(features_csv, updated_features_csv):
    with open(updated_features_csv, 'a') as fout:
        with open(features_csv, 'r') as fin:
            for line in fin:
                new_line = line.replace('[', '').\
                replace(']','').replace('\'', '').\
                replace('\"','').replace('{','').\
                replace('}','').replace('(','').\
                replace(')','').replace('*','').\
                replace('%','')
                fout.write(new_line)
    return

def organize_features(updated_features_csv, feature_mapping_csv, features_integers_mapping):
    header = []
    removed_index = []
    tag_names_index = []
    top_row = True
    instance_mapping_dict = utilities.read_json(features_integers_mapping)

    common_tag_names = {'body', 'document', 'div', 'iframe', 'script', 'input', 'html', 'style', 'header', 'a', 'button', 'ul', 'li', 'span', 'header', 'img', 'section', 'form', 'table', 'h1', 'h2'}
    canvas = 'canvas'
    # canvas, common, uncommon - 0,1,2
    non_numeric = {'fcu123', 'fcu152', 'fcu2', 'faca16', 'fcu80', 'fcu57', 'fcu24', 'fcu83', 'fcu48', 'fcu30', 'fcu148', 'fcu136', 'faca44', 'fvca5'}

    temp = 0
    k = 0
    with open(updated_features_csv, 'r') as fin:
        for line in fin:
            k += 1
    
    pbar = tqdm(total=k)

    with open(feature_mapping_csv, 'a') as fout:
        with open(updated_features_csv, 'r') as fin:
            for line in fin:
                if top_row:
                    top_row = False
                    raw_header = line.split(',')
                    for idx, item in enumerate(raw_header):
                        if item.strip().split('_')[0] != 'fvca15':
                            header.append(item.strip())
                            if item.strip().split('_')[0] == 'fvca5' or item.strip().split('_')[0] == 'faca44':
                                tag_names_index.append(idx)
                        else:
                            removed_index.append(idx)
                    fout.write(','.join(header) + '\n')
                else:
                    temp += 1
                    raw_splitted_line = line.strip().split(',')
                    splitted_line = []
                    for i, item in enumerate(raw_splitted_line):
                        if i not in removed_index:
                            splitted_line.append(item)

                    for idx, item in enumerate(splitted_line):
                        if idx == 0 or idx == 1 or idx == len(splitted_line) -1:
                            continue
                        if header[idx].strip().split('_')[0] not in non_numeric and utilities.isfloat(item):
                            if header[idx] in instance_mapping_dict:
                                if instance_mapping_dict[header[idx]]['type'] == 'nominal':
                                    print('We have a problem - nominal to numeric')
                                    print(header[idx])
                            else:
                                print('Anomaly, but should not happen much. Perhaps, not at all')
                                print(header[idx])
                                # instance_mapping_dict[header[idx]] = {}
                                # instance_mapping_dict[header[idx]]['type'] = 'numeric'
                                # instance_mapping_dict[header[idx]]['items'] = []
                        elif item.strip() == '':
                            continue

                        else:
                            if header[idx] in instance_mapping_dict:

                                if instance_mapping_dict[header[idx]]['type'] == 'numeric':
                                    print('We have a problem - numeric to nominal')
                                    print(header[idx])
                                else:
                                    if header[idx] in instance_mapping_dict and item.strip() not in instance_mapping_dict[header[idx]]['items']:
                                        # instance_mapping_dict[header[idx]]['items'].append(item.strip())
                                        print('Anomaly, but should not happen much. Perhaps, not at all. No need to add additional items - should keep things that we have already seen.')

                                    if idx in tag_names_index:
                                        if item.strip().lower() == 'canvas':
                                            splitted_line[idx] = 0
                                        elif item.strip().lower() in common_tag_names:
                                            splitted_line[idx] = 1
                                        else:
                                            splitted_line[idx] = 2
                                    else: 
                                        if header[idx] in instance_mapping_dict:
                                            if item.strip() in instance_mapping_dict[header[idx]]['items']:
                                                splitted_line[idx] = instance_mapping_dict[header[idx]]['items'].index(item.strip())
                                            else:
                                                splitted_line[idx] = ''
                            else:
                                # instance_mapping_dict[header[idx]] = {}
                                # instance_mapping_dict[header[idx]]['type'] = 'nominal'
                                # instance_mapping_dict[header[idx]]['items'] = [item.strip()]
                                print('Anomaly, but should not happen much. Perhaps, not at all. No need to add additional items - should keep things that we have already seen.')

                                if idx in tag_names_index:
                                    if item.strip().lower() == 'canvas':
                                        splitted_line[idx] = 0
                                    elif item.strip().lower() in common_tag_names:
                                        splitted_line[idx] = 1
                                    else:
                                        splitted_line[idx] = 2
                                else:
                                    if header[idx] in instance_mapping_dict:
                                        if item.strip() in instance_mapping_dict[header[idx]]['items']:
                                            splitted_line[idx] = instance_mapping_dict[header[idx]]['items'].index(item.strip())
                                        else:
                                            splitted_line[idx] = ''

                    fout.write(','.join(str(e) for e in splitted_line) + '\n')
                pbar.update(1)
    return

# Not using the scikit built in because want to keep the mapping for later usage
def one_hot_encoder(updated_features_csv, feature_mapping_csv, features_integers_mapping):    
    k = 0
    with open(updated_features_csv, 'r') as fin:
        for line in fin:
            k += 1
    
    pbar = tqdm(total=k)

    top_row = True
    features_mapping = utilities.read_json(features_integers_mapping)
    header = []
    new_features = []
    with open(feature_mapping_csv, 'a') as fout:
        with open(updated_features_csv, 'r') as fin:
            for line in fin:
                if top_row:
                    top_row = False
                    raw_header = line.strip().split(',')
                    for idx, item in enumerate(raw_header):
                        if item in features_mapping:
                            expansion_length = len(features_mapping[item]['items'])
                            if expansion_length > 1:
                                if item.split('_')[0] == 'fvca5' or item.split('_')[0] == 'faca44':
                                    expansion_length = 3

                                for i in range(expansion_length):
                                    new_features.append(item + '+' + str(i))
                        else:
                            print('This should not happen, except for few features')
                            # because we consider the max number of API calls and ony consider the first occurance of script execution
                            # the max calls may be generated by same script on some other domain
                    header = raw_header[:-1] + new_features + ['class']
                    fout.write(','.join(header) + '\n')
                    len_new_features = len(new_features)
                    print(len(header))
                    print(','.join(header))

                else:
                    raw_splitted_line = line.strip().split(',')
                    new_line = line.strip().split(',')[:-1] + ([0] * len_new_features) + raw_splitted_line[-1:]

                    for idx, item in enumerate(raw_splitted_line):
                        item_to_check = header[idx]

                        if item_to_check in features_mapping:
                            expansion_length = len(features_mapping[item_to_check]['items'])
                            if expansion_length > 1:
                                if item.strip() != '': # and item_to_check + '+' + str(item)) in header:
                                    new_line[header.index(item_to_check + '+' + str(item))] = 1
                                new_line[idx] = ''
                    fout.write(','.join(str(e) for e in new_line) + '\n')
                pbar.update(1)
    return

def convert_to_arff(updated_features_csv, arff_addr, features_integers_mapping):
    hashes = set()
    urls = set()
    features_mapping = utilities.read_json(features_integers_mapping)
    
    head_row = True
    header = ''
    with open(updated_features_csv, 'r') as fin:
        for line in fin:
            if head_row:
                header = line
                head_row = False
            else:
                tmp = line.split(',',3)
                if tmp[0] != '':
                    hashes.add(tmp[0])
                if tmp[1] != '':
                    urls.add(tmp[1])

    columns_to_write = []
    columns_to_write.append('@relation features_properties')
    columns_to_write.append('')
    print(len(header.strip().split(',')))
    print(header)
    for line in header.strip().split(','):
        if line == 'hash':
            columns_to_write.append('@attribute ' + line + ' {' + ','.join(hashes) + '}')        
        elif line == 'url_id':
            columns_to_write.append('@attribute ' + line + ' {' + ','.join(urls) + '}')
        
        # elif line in features_mapping:
            # expansion_length = len(features_mapping[line]['items'])
            # if expansion_length > 1:
            #     if line.split('_')[0] == 'fvca5' or line.split('_')[0] == 'faca44':
            #         expansion_length = 3
                
            #     columns_to_write.append('@attribute ' + line + ' {' + ','.join(str(i) for i in range(expansion_length)) + '}')
            # else:
            # columns_to_write.append('@attribute ' + line + ' numeric')
        elif line == 'class':
            columns_to_write.append('@attribute ' + line + ' {FP,NONFP}') 
        else:
            columns_to_write.append('@attribute ' + line + ' numeric')

    print(len(columns_to_write))
    columns_to_write.append('')
    columns_to_write.append('@data')
    columns_to_write.append('')
    utilities.append_list(arff_addr, columns_to_write)

    status = True
    rows_to_write = []
    
    with open(arff_addr, "a") as myfile:
        with open(updated_features_csv) as f:
            for line in f:            
                if status:
                    status = False
                else:                    
                    if ',,' in line:
                        empty_spaces = line.strip().split(',')
                        empty_space_line = ['?' if x == '' else str(x) for x in empty_spaces]
                        line = ','.join(empty_space_line)
                    myfile.write(line.strip()+ '\n')
    return

def main():
    data_directory =  sys.argv[1] # path to partitioned data
    # class_labels =  sys.argv[2]
    dynamic_feature_mapping_file = os.path.join(data_directory, 'dynamic_feature_mapping.json')  # assume this file is present , copy this file to ec2 instance
    js_api_count_file = os.path.join(data_directory, 'maximum_number_of_api_calls.json')
    url_index_mapping = os.path.join(data_directory, 'url_index_mapping.txt')
    features_csv = os.path.join(data_directory, 'dynamic_features.csv')
    updated_features_csv = os.path.join(data_directory, 'updated_dynamic_features.csv')
    arff_addr = os.path.join(data_directory, 'features_with_encoding.arff')
    feature_mapping_csv =  os.path.join(data_directory, 'dynamic_features_with_mappings.csv')
    feature_csv_encoding =  os.path.join(data_directory, 'features_with_encoding.csv')
    features_integers_mapping =  os.path.join(data_directory, 'features_integers_mapping.json')

    #### create_mapping_of_properties(dynamic_feature_mapping_file) # assume this file is present , copy this file to ec2 instance
    #### count_feature_occurances(data_directory, js_api_count_file) # No need to run it - if needed just cipy the file to ec2 instance 
    
    # NEED TO RUN
    feature_mapping = utilities.read_json(dynamic_feature_mapping_file) # just read from file here
    global_symbols_count = utilities.read_json(js_api_count_file) # just read from file here
    
    # construct_features(data_directory, feature_mapping, global_symbols_count, url_index_mapping, features_csv)
    # remove_unwanted_characters_from_csv(features_csv, updated_features_csv)

    # organize_features(updated_features_csv, feature_mapping_csv, features_integers_mapping)
    # one_hot_encoder(feature_mapping_csv, feature_csv_encoding, features_integers_mapping)
    convert_to_arff(feature_csv_encoding, arff_addr, features_integers_mapping)

if __name__ == '__main__':
    main()