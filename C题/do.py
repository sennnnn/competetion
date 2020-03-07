import os
import csv
import sys
import time

from util import csv_preprocss, string_preprocess, record_word_frequency

item_path = sys.argv[1]
file_length = int(sys.argv[2])

if(not os.path.exists(item_path)):
    assert False, "第一个命令行参数必须输入有效路径"

col = csv.register_dialect('mydialect',delimiter='\t',quoting=csv.QUOTE_ALL)

info_dict = None
info_length = 0
valid_line = []
with open(item_path, 'r') as f:
    file_list  = csv.reader(f, 'mydialect')
    valid_line.append(next(file_list))
    valid_length = len(valid_line[0])
    for i in range(file_length):
        try:
            content = next(file_list)
            if(len(content) != valid_length): continue
            valid_line.append(content) 
            info_length += 1
        except:
            print("{} line bad.".format(i+1))
        
    info_dict = csv_preprocss(valid_line)

base_name = os.path.split(item_path)[1].split('.')[0]

with open(base_name + '_benchmark.txt', 'w') as f:
    for line in valid_line:
        line = ''.join([x+'\t' for x in line])
        f.write(line + '\n')

with open(base_name + '.txt', 'w') as f:
    f.write('marketplace customer_id string encode\n')
    string = ""
    length = 0
    word_list = []
    line_list = []
    start = time.time()
    for i in range(info_length):
        market_info = info_dict['marketplace'][i]
        customer_id_info = info_dict['customer_id'][i]
        string = info_dict['review_body'][i]
        string = string_preprocess(string)
        line_list.append([market_info, customer_id_info, string])
        for word in string:
            word_list.append(word)
    end = time.time()

    word_list_sorted = record_word_frequency(word_list, base_name + '_word_info.txt')

    for line in line_list:
        encode_list = [str(word_list_sorted.index(x)) + '_' for x in line[-1]]
        encode_str = ''.join(encode_list)
        f.write('{} {} {} {}\n'.format(*tuple(line), encode_str))
