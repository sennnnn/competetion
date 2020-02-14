import csv
import sys

from util import csv_process,team_member_get,team_key_word_extract,cooperation_detect,\
                 catch_ball_time_calculate,average

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

OriginPlayerID_all = [x['OriginPlayerID'] for x in all_info]
DesinationPlayerID_all = [x['DestinationPlayerID'] for x in all_info]

team_members = team_member_get(OriginPlayerID_all, DesinationPlayerID_all, team_name)

sys_args = sys.argv[1:]

flag_cooperation_pass = True if('--coop_pass' in sys_args) else False
flag_pass_origin_dest_per_team_member = True if('--pass_ori_dst_pm' in sys_args) else False
flag_attractive_force_item_per_team_member = True if('--attrc_force_item_pm' in sys_args) else False
flag_event_coordinate_per_player = True if('--coordinate_per_op' in sys_args) else False

# 队伍综合能力
# 队伍传球能力：累计传球次数
# 队伍配合能力：累计配合次数，二人配合 + 三人配合
# 小队配合能力：二人配合次数，三人配合次数
# 个人配合能力：传球次数，接球次数
if(flag_cooperation_pass):
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

    f = open('{}/{}_cooperation&pass_count.txt'.format(result_path, team_name), 'w', encoding='utf-8')
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

if(flag_pass_origin_dest_per_team_member):
    f = open('{}/{}_pass_origin.txt'.format(result_path, team_name), 'w', encoding='utf-8')
    f_ = open('{}/{}_pass_dest.txt'.format(result_path, team_name), 'w', encoding='utf-8')

    f.write('这个是传出的记录!\n\n========================================================================\n')
    f_.write('这个是接住的记录!\n\n========================================================================\n')

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

if(flag_attractive_force_item_per_team_member):
    f = open('{}/{}_attractive_force_item.txt'.format(result_path, team_name), 'w', encoding='utf-8')
    pass_type_list = ['Head pass', 'Simple pass', 'Launch', 'High pass', 'Hand pass', 'Smart pass', 'Cross']
    single_member_attract_items = {member:{'catch_ball_time':0, 'attend_race_ID_list':[], \
                                'pass_all_kind_count':{pass_type:0 for pass_type in pass_type_list}} for member in team_members}

    for i in range(len(all_info)):
        # 统计传球种类
        info_temp = all_info[i]
        origin_player_ID = info_temp['OriginPlayerID']
        if(team_name not in origin_player_ID):
            continue
        # 统计出场 ID
        race_id = info_temp['MatchID']
        if(race_id not in single_member_attract_items[origin_player_ID]['attend_race_ID_list']):
            single_member_attract_items[origin_player_ID]['attend_race_ID_list'].append(race_id)
        pass_type = info_temp['EventSubType']
        single_member_attract_items[origin_player_ID]['pass_all_kind_count'][pass_type] += 1
        # 统计带球时间
        if(i == 0):
            continue
        info_1 = all_info[i-1]
        info_2 = all_info[i]
        race_id_1 = info_1['MatchID']
        race_id_2 = info_2['MatchID']
        if(race_id_1 != race_id_2):
            continue
        for member in team_members:
            flag,time = catch_ball_time_calculate(info_1, info_2, member)
            if(flag and time > 0):
                single_member_attract_items[member]["catch_ball_time"] += time

    for member in team_members:
        f.write('[{}]\n'.format(member))
        f.write('持球时间 = {}\n'.format(single_member_attract_items[member]['catch_ball_time']))
        f.write('参赛次数 = {}\n'.format(len(single_member_attract_items[member]['attend_race_ID_list'])))
        f.write('传球各种类触发次数统计：\n')
        temp = single_member_attract_items[member]['pass_all_kind_count']
        temp_string_ = '一下按顺序分别为：\n'
        temp_string = ''
        for key in temp.keys():
            temp_string_ += ' {} |'.format(key)
            temp_string += '{} '.format(temp[key])
        f.write('{}\n'.format(temp_string_))
        f.write('{}\n'.format(temp_string))
        f.write('\n')

    f.close()

if(flag_event_coordinate_per_player):
    f = open('{}/{}_coordinate_origin_dest_avg.txt'.format(result_path, team_name), 'w', encoding='utf-8')
    # 'OriginPlayerID', 'DestinationPlayerID'
    # 'EventOrigin_x', 'EventOrigin_y', 'EventDestination_x', 'EventDestination_y'
    coordinate_per_player = {member:{'origin':[], 'dest':[]} for member in team_members}
    coordinate_avg_per_player = {member:{'origin':None, 'dest':None} for member in team_members}
    for line in all_info:
        origin_player_ID = line['OriginPlayerID']
        dest_player_ID = line['DestinationPlayerID']
        if(team_name not in origin_player_ID or team_name not in dest_player_ID):
            continue
        origin_x = float(line['EventOrigin_x'])
        origin_y = float(line['EventOrigin_y'])
        dest_x = float(line['EventDestination_x'])
        dest_y = float(line['EventDestination_y'])
        coordinate_per_player[origin_player_ID]['origin'].append((origin_x, origin_y))
        coordinate_per_player[dest_player_ID]['dest'].append((dest_x, dest_y))
    
    for member in team_members:
        origin_temp = coordinate_per_player[member]['origin']
        dest_temp = coordinate_per_player[member]['dest']
        coordinate_avg_per_player[member]['origin'] = (average([x[0] for x in origin_temp]), \
                                                       average([x[1] for x in origin_temp])) 
        coordinate_avg_per_player[member]['dest']   = (average([x[0] for x in dest_temp]), \
                                                       average([x[1] for x in dest_temp]))        
    
    f.write('队伍成员传接球站位统计!!\n=========================================================\n')
    for member in team_members:
        f.write('[{}]\n'.format(member))
        f.write('传球平均坐标：x:{} y:{}\n'.format(*coordinate_avg_per_player[member]['origin']))
        f.write('传球平均坐标：x:{} y:{}\n'.format(*coordinate_avg_per_player[member]['dest']))
        f.write('\n')
    f.close()