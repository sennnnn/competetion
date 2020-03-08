import os
import sys

from util import col_extract,txt_get,parse_score

task = int(sys.argv[1])

ha_path = 'build/hair_dryer.txt'
mi_path = 'build/microwave.txt'
pa_path = 'build/pacifier.txt'

txt_content = None
if(task == 0):
    # hair_dryer
    filepath = ha_path
    ha_word_score_table = os.path.splitext(filepath)[0] + '_word_selected.txt'
    txt_content = txt_get(ha_word_score_table)
elif(task == 1):
    # microwave
    filepath = mi_path
    mi_word_score_table = os.path.splitext(filepath)[0] + '_word_selected.txt'
    txt_content = txt_get(mi_word_score_table)
elif(task == 2):
    # pacifier
    filepath = pa_path
    pa_word_score_table = os.path.splitext(filepath)[0] + '_word_selected.txt'
    txt_content = txt_get(pa_word_score_table)
else:
    assert False, "Error, task number must be [0(hair_dryer)/1(microwave)/2(pacifier)]."

score_dict = parse_score(txt_content)
save_name = os.path.splitext(os.path.split(filepath)[1])[0]

f = open(filepath, 'r')
lines = f.readlines()

# 将单词处理成列表
valid_lines = lines[1:]
line_word = col_extract(valid_lines)
# 最后要写入文本文件的行
write_lines = lines[1:]
temp = []
for line in write_lines:
    temp.append('{} {}'.format(*tuple(line.split()[:2])))
write_lines = temp

for i in range(len(line_word)):
    score_keys = score_dict.keys()
    score = 0
    for word in line_word[i]:
        flag = 0
        for key in score_keys:
            if(word in score_dict[key]):
                score += key
                flag = 1
                break
        if(flag): continue

    write_lines[i] += ' {}'.format(score)

f = open('build/{}_processed.txt'.format(save_name), 'w')
f.write(''.join([line+'\n' for line in write_lines]))
f.close()