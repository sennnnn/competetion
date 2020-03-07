import os
import sys

from util import col_extract

score_dict = {1:['happy'], 2:['the'], -1:["can't", 'no']}

filepath = sys.argv[1]
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

f = open('{}_processed.txt'.format(save_name), 'w')
f.write(''.join([line+'\n' for line in write_lines]))
f.close()