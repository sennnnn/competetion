import os
import sys

from util import col_extract

# hair_dryer
# score_1=['happy','love','beautiful','beauty','good','well','easy','powerful','quickly','fast','cool','fine','new','quiet','compact','lightweight','strong','super','quite','cheap','loved','feature','smooth','warm','professional','easily','soft','liked','loves','pleased','quick','shiny','fit','awesome','glad','already','believable','beneficial','terrisic','benevolent','benevolently','impressed','clean','gift','convenient','kind','natural','satisfied','bright','thank','handy','nicely','plenty','thanks','comfortable','surprised','okay','decent','fantastic','silky','available','likes','reasonable','inexpensive','please','figured','naturally','ready','original','efficient','healthy','excited','useful','special','durable','reliable','adjustable','positive','fancy','effective','honestly','reasonably','wide','properly','hopefully','authorized','surprise','convenience','amazed']
# score_2=['great','nice','best','perfect','pretty','excellent','amazing','perfectly','thrilled','fabulous']
# score_n1=['broke', 'died', 'bad', 'disappointed', 'noisy', 'difficult', 'damage',  'burning', 'waste',  'burn', 'burned', 'negative','blast',  'stuck',  'coarse', 'damaged', 'smoke', 'con', 'defective', 'refund', 'junk', 'worst', 'flimsy', 'skeptical', 'poor',  'horrible', 'die', 'vanity', 'failed', 'hassle', 'dead', 'worry', 'breaking', 'werid', 'disappointing', 'worse', 'tangle', 'overly','damaging', 'frustrating', 'overheating',  'lack', 'flaw', 'worried', 'disappointment', 'suck', 'trash', 'split', 'fault', 'uncomfortable', 'slowly', 'slowly', 'complained', 'downside', 'dies', 'popping', 'stiff', 'burst',  'odd', 'garbage']

# microwave
# score_1=['like','well','good','easy','nice','fit','love','fine','stainless','happy','pretty','simple','powerful','worth','easily','quickly','pleased','available','ok','compact','definitely','cheap','simply','evenly','exact','quick','quiet','cool','properly','thanks','satisfied','please','normal','convenient','attractive','nicely','thank','strong','cute','faster','beautiful','surprised','special','safety','okay','automatically']
# score_2=['great','perfect','perfectly','best','excellent','wonderful']
# score_n1=['problem','old','sharp','problems','bad','hard','issues','expensive','failed','short','error','defrost','damaged','complaints','poor','heavy','wrong','difficult','broken','negative','disappointed','smell','noisy','junk','unfortunately','complaint','cracked','break','burning','worse','damage','defective','terrible','sorry','mistake','fail','burn','horrible','smoke','disappointing','burnt','awesome','dangerous']

# score_1=['great', 'like', 'love', 'loves', 'easy', 'cute', 'perfect', \
#          'clean', 'loved', 'better', 'best', 'soft', 'easily', 'fit', \
#          'likes', 'easier', 'pretty', 'favorite', 'wanted', 'want', \
#          'adorable', 'comfortable', 'atttached', 'helps', 'awesome', \
#          'free', 'safe','perfectly', 'excellent', 'fun', 'durable', \
#          'glad', 'natural', 'cheap', 'thank', 'amazing', 'pleased', \
#          'bright', 'thanks', 'safety', 'real',  'helped', 'comfort', \
#          'warm', 'strong', 'cheaper', 'available', 'excited', 'working', \
#          'useful', 'cool', 'beautiful', 'convenient', 'lightweight', \
#          'nicely',  'secure', 'enjoy', 'soothe', 'important', 'soothing', \
#          'fantastic',  'satisfied', 'enjoys', 'pros','adjustable','compliments',\
#          'properly','interested','plenty','smooth','impressed','please','cutest',\
#          'surprised','quiet','comfy','sweet','calm','colorful','decent','flexible',\
#          'enjoyed','practical','peace','interest','affordable','clearly','comfortably',\
#          'compact','security','cheaply','friendly','happier','effective','wonderfully',\
#          'securely','positive','soothed','happily','nicer','attractive','excelent']
# score_2 = []
# score_n1=['hard', 'never', 'difficult', 'disappointed', 'heavy', 'bad', 'expensive', 'problems', 'issues', 'unfortunately', 'worry', 'stuck','wrong', 'leak', 'noise', 'dirty','broke','waste', 'break', 'harder', 'complaint','tight', 'trouble', 'bulky', 'pain', 'annoying', 'cold', 'snap', 'crying', 'loose', 'leaks', 'returned', 'hate', 'worried', 'crazy', 'useless','broken','hated','poor','negative','pricey','complaints','hurt','losing','mess','choking','horrible','uncomfortable','refused','downside','bother','hassle','awkward','upset','worn','disappointing','hazard','afraid','tired','terrible','stiff','fault','frustrating','complain','silly','smells','sadly','worse','risk','dangerous','dirt','worst','awful','frustrated','regret','germs','damaged','damage','messy','rejected']

# score_dict = {1:score_1, 2:score_2, -1:score_n1}
# score_dict = {1:score_1+score_2, 2:[], -1:score_n1}
score_dice = {}

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