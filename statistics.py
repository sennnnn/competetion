import csv

from util import csv_process,team_member_get,team_key_word_extract,cooperation_detect

fullevents_path = 'data/fullevents.csv'
matches_path = 'data/matches.csv'
passingevents_path = 'data/passingevents.csv'

csv_file = csv.reader(open(passingevents_path, 'r'))

all_info = list(csv_file)

team_name = 'Husk'

result_path = 'result'

# 总共有这么些数据项目
# ['MatchID', 'TeamID', 'OriginPlayerID', 'DestinationPlayerID', 'MatchPeriod', 'EventTime', \
# 'EventSubType', 'EventOrigin_x', 'EventOrigin_y', 'EventDestination_x', 'EventDestination_y']

all_info = csv_process(all_info)

# 队伍综合能力
# 队伍传球能力：累计传球次数
# 队伍配合能力：累计配合次数，二人配合 + 三人配合
# 小队配合能力：二人配合次数，三人配合次数
# 个人配合能力：传球次数，接球次数

team_key_word_list = ['Husk', 'Oppo']
team_pass_count = {'Husk':0, 'Oppo':0}
team_cooperation_count = {'Husk':{2:0, 3:0}, 'Oppo':{2:0, 3:0}}
team_cooperation_list = {'Husk':[], 'Oppo':[]}


for i in range(len(all_info)):
    # 统计传球次数
    Origin_player = all_info[i]['OriginPlayerID']
    team_key_word = team_key_word_extract(Origin_player)
    team_pass_count[team_key_word] += 1
    if(i == 0):
        continue
    # 统计合作次数
    info_1 = all_info[i-1]
    info_2 = all_info[i]
    players,flag = cooperation_detect(info_1, info_2)
    if(flag):
        team_cooperation_list[team_key_word].append((i+1, tuple(players)))
        team_cooperation_count[team_key_word][len(players)] += 1

print(team_pass_count)
print(team_cooperation_count)

f = open('{}/cooperation&pass_count.txt'.format(result_path), 'w', encoding='utf-8')
f.write('p.s. 注意 Oppo 是敌队的意思。\n传球次数统计：\n{}队:{}  {}队:{}\n\n'.format('Husk', team_pass_count['Husk'], \
                                                                                'Oppo', team_pass_count['Oppo']))

f.write('配合次数统计：\n{}队：二元配合：{} 三元配合：{}  {}队：二元配合：{} 三元配合{}\n\n'\
                            .format('Husk', team_cooperation_count['Husk'][2], team_cooperation_count['Husk'][3], \
                                    'Oppo', team_cooperation_count['Oppo'][2], team_cooperation_count['Oppo'][3]))
f.write('!!! 以下是配合明细 !!!\n================================================================================\n')

two_player_cooperation_list = []
tri_player_cooperation_list = []
for one in team_cooperation_list[team_name]:
    raw_line_number = one[0]
    players = list(one[1])
    cooperation_player_number = len(players)
    if(cooperation_player_number == 2):
        players.append(players[0])
        two_player_cooperation_list.append((raw_line_number, cooperation_player_number, tuple(players)))
        continue
    tri_player_cooperation_list.append((raw_line_number, cooperation_player_number, tuple(players)))

[f.write("raw_line_number:{} cooperation_player_number:{} {}==>{}==>{}\n".format(a, b, *c)) \
    for a,b,c in two_player_cooperation_list]

[f.write("raw_line_number:{} cooperation_player_number:{} {}==>{}==>{}\n".format(a, b, *c)) \
    for a,b,c in tri_player_cooperation_list]

f.close()


f = open('{}/{}_pass_origin.txt'.format(result_path, team_name), 'w', encoding='utf-8')
f_ = open('{}/{}_pass_dest.txt'.format(result_path, team_name), 'w', encoding='utf-8')

f.write('这个是传出的记录!\n\n========================================================================\n')
f_.write('这个是接住的记录!\n\n========================================================================\n')

OriginPlayerID_all = [x['OriginPlayerID'] for x in all_info]
DesinationPlayerID_all = [x['DestinationPlayerID'] for x in all_info]

team_members = team_member_get(OriginPlayerID_all, DesinationPlayerID_all, team_name)

# 传球统计
playerwise_pass_origin_count = {member:{member_:0 for member_ in team_members} for member in team_members}
# 接球统计
playerwise_pass_dest_count  = {member:{member_:0 for member_ in team_members} for member in team_members}
for member in team_members:
    playerwise_pass_origin_count[member]['all'] = 0
    playerwise_pass_dest_count[member]['all'] = 0

for i,j in zip(OriginPlayerID_all, DesinationPlayerID_all):
    if(team_name not in i or team_name not in j):
        continue

    # 传出
    playerwise_pass_origin_count[i][j] += 1
    playerwise_pass_origin_count[i]['all'] += 1
    # 接到
    playerwise_pass_dest_count[j][i] += 1
    playerwise_pass_dest_count[j]['all'] += 1

for member in team_members:
    f.write('[{}]\n'.format(member))
    f_.write('[{}]\n'.format(member))
    member_dict = playerwise_pass_origin_count[member]
    member_dict_ = playerwise_pass_dest_count[member]
    for i,j in zip(member_dict.keys(), member_dict_.keys()):
        f.write('{}:{}\n'.format(i, member_dict[i]))
        f_.write('{}:{}\n'.format(j, member_dict_[j]))
    f.write('\n')
    f_.write('\n')
f.close()
f_.close()