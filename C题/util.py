import re

letter_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', \
            'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

def csv_preprocss(csv_list):
    item_list = csv_list[0]
    info_dict = {}
    for item in item_list:
        info_dict[item] = []

    for line in csv_list[1:]:
        for i in range(len(item_list)):
            info_dict[item_list[i]].append(line[i])

    return info_dict

def itemwise_split(string_list, split_letter):
    temp = [x.split(split_letter) for x in string_list]
    string = []
    for x in temp:
        string = string + x
    
    return string

def string_preprocess(string):
    string = string.replace('(', ' ')
    string = string.replace(')', ' ')
    string = string.replace('（', ' ')
    string = string.replace('）', ' ')
    string = string.replace('\\', ' ')
    string = string.replace(',', ' ')
    string = string.replace('.', ' ')
    string = string.replace('!', ' ')
    string = string.replace('?', ' ')
    string = string.replace('-', ' ')
    string = string.replace(':', ' ')
    string = string.replace('[', ' ')
    string = string.replace(']', ' ')
    string = string.replace(';', ' ')
    string = string.replace('\"', ' ')
    string = string.replace('&#34', ' ')
    string = string.replace('~', ' ')
    temp = string.split('<br />')
    temp = itemwise_split(temp, '<BR>')
    temp = itemwise_split(temp, ' ')
    temp = itemwise_split(temp, '/')

    best_string = []
    for word in temp:
        flag = 1
        for letter in word:
            if(letter.lower() in letter_list): flag = 0
        
        if(flag == 1): continue
        # 统一弄成小写
        best_string.append(''.join([x.lower() for x in word]))

    return best_string

def record_word_frequency(word_list, file_path):
    # 去掉重复元素
    word_set = set(word_list)
    word_dict = {item: word_list.count(item) for item in word_set}
    # [(word: frequency), ...]
    word_tuple = sorted(word_dict.items(), key=lambda x: x[1], reverse=True)

    f = open(file_path, 'w')
    for i in range(len(word_tuple)):
        f.write('{} {} {}\n'.format(word_tuple[i][0], word_tuple[i][1], i))

    word_list_sorted = [x[0] for x in word_tuple]

    return word_list_sorted

def col_extract(lines): 
    ret = []
    for line in lines:
        cols = line.split(' ')
        col = ''.join(cols[2:-1])
        ret.append(eval(col))
    
    return ret

def txt_get(txt_path):
    f = open(txt_path, 'r')
    
    return f.read()

def parse_score(txt_content):
    score_dict = {}
    pattern = 'score_.*=\[.*\]'
    pattern_obj = re.compile(pattern)
    result = pattern_obj.findall(txt_content)
    for s in result:
        flag = 1
        head = s.split('=')[0]
        tail = s.split('=')[1]
        head = head.replace('score_', '')
        if('n' in head): 
            flag = -1
            head = head.replace('n', '')
        score_dict[flag*int(head)] = eval(tail)
    
    return score_dict
