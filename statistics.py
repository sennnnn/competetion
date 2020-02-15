import csv
import sys

from util import csv_process,team_member_get,team_key_word_extract,cooperation_detect,\
                 catch_ball_time_calculate,average,Matchwise_all_info_get,MatchID_list_get,\
                 Matchwise_team_members_get,origin_or_dest_team_member_get

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

MatchID_list = MatchID_list_get(all_info)

Matchwise_all_info = Matchwise_all_info_get(all_info)

sys_args = sys.argv[1:]

flag_cooperation_pass = True if('--coop_pass' in sys_args) else False
flag_pass_origin_dest_per_team_member = True if('--pass_ori_dst_pm' in sys_args) else False
flag_attractive_force_item_per_team_member = True if('--attrc_force_item_pm' in sys_args) else False
flag_event_coordinate_per_player = True if('--coordinate_per_op' in sys_args) else False

# 队伍综合能力
# 队伍传球能力：每一场传球次数
# 队伍配合能力：每一场配合次数，二人配合 + 三人配合
# 小队配合能力：二人配合次数，三人配合次数
# 个人配合能力：传球次数，接球次数
if(flag_cooperation_pass):
    team_key_word_list = ['Husk', 'Oppo']
    team_pass_count = {'Husk':[], 'Oppo':[]}
    team_cooperation_count = {'Husk':{2:[], 3:[]}, 'Oppo':{2:[], 3:[]}}
    team_cooperation_list = {'Husk':[], 'Oppo':[]}

    old_MatchID = 0

    for i in range(len(all_info)):
        Origin_player = all_info[i]['OriginPlayerID']
        team_key_word = team_key_word_extract(Origin_player)
        MatchID = int(all_info[i]['MatchID'])
        if(old_MatchID != MatchID):
            team_pass_count['Husk'].append(0)
            team_pass_count['Oppo'].append(0)
            team_cooperation_count['Husk'][2].append(0)
            team_cooperation_count['Oppo'][2].append(0)
            team_cooperation_count['Husk'][3].append(0)
            team_cooperation_count['Oppo'][3].append(0)
            team_cooperation_list['Husk'].append([])
            team_cooperation_list['Oppo'].append([])
            old_MatchID = MatchID
        # 统计传球次数
        team_pass_count[team_key_word][MatchID-1] += 1
        if(i == 0):
            continue
        # 统计合作次数
        info_1 = all_info[i-1]
        info_2 = all_info[i]
        players,flag = cooperation_detect(info_1, info_2)
        if(flag):
            team_cooperation_list[team_key_word][MatchID-1].append((i+1, tuple(players)))
            team_cooperation_count[team_key_word][len(players)][MatchID-1] += 1

    print(team_pass_count)
    print(team_cooperation_count)
    
    f = open('{}/{}_cooperation&pass_count.txt'.format(result_path, team_name), 'w', encoding='utf-8')
    f.write('p.s. 注意 Oppo 是敌队的意思。\n')
    f.write('[传球次数统计] \n比赛场次 | {}队 | {}队\n'.format('Husk', 'Oppo'))
    for MatchID in MatchID_list:
        f.write('{}  {}  {}\n'.format(MatchID, team_pass_count['Husk'][MatchID-1], team_pass_count['Oppo'][MatchID-1]))

    f.write('\n')

    f.write('[配合次数统计] \n比赛场次 | {}队二元配合 | {} 队二元配合 | {} 队三元配合 | {} 队三元配合\n'\
            .format('Husk', 'Oppo', 'Husk', 'Oppo'))    
    for MatchID in MatchID_list:
        f.write('{} {} {} {} {}\n'.format(MatchID, \
                                     team_cooperation_count['Husk'][2][MatchID-1], team_cooperation_count['Oppo'][2][MatchID-1], \
                                     team_cooperation_count['Husk'][3][MatchID-1], team_cooperation_count['Oppo'][3][MatchID-1]))
        
    # f.write('!!! 以下是配合明细 !!!\n================================================================================\n')

        # two_player_cooperation_list = []
        # tri_player_cooperation_list = []
        # for one in team_cooperation_list[team_name]:
        #     raw_line_number = one[0]
        #     players = list(one[1])
        #     cooperation_player_number = len(players)
        #     if(cooperation_player_number == 2):
        #         players.append(players[0])
        #         two_player_cooperation_list.append((raw_line_number, cooperation_player_number, tuple(players)))
        #         continue
        #     tri_player_cooperation_list.append((raw_line_number, cooperation_player_number, tuple(players)))

        # [f.write("raw_line_number:{} cooperation_player_number:{} {}==>{}==>{}\n".format(a, b, *c)) \
        #     for a,b,c in two_player_cooperation_list]

        # [f.write("raw_line_number:{} cooperation_player_number:{} {}==>{}==>{}\n".format(a, b, *c)) \
        #     for a,b,c in tri_player_cooperation_list]

        # f.close()

if(flag_pass_origin_dest_per_team_member):
    f = open('{}/{}_pass_origin.txt'.format(result_path, team_name), 'w', encoding='utf-8')
    f_ = open('{}/{}_pass_dest.txt'.format(result_path, team_name), 'w', encoding='utf-8')

    f.write('这个是传出的记录!\n')
    f_.write('这个是接住的记录!\n')

    for MatchID in MatchID_list:
        f.write('\n========================================================================\n')
        f_.write('\n========================================================================\n')
        f.write('[{}]\n\n'.format(MatchID))
        f_.write('[{}]\n\n'.format(MatchID))
        single_Match_all_info = Matchwise_all_info[MatchID-1]

        team_members,OriginPlayerID_all,DesinationPlayerID_all = \
        Matchwise_team_members_get(single_Match_all_info, team_name)

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
    
    for MatchID in MatchID_list:

        f.write('[{}]\n\n'.format(MatchID))

        single_Match_all_info = Matchwise_all_info[MatchID-1]

        team_members,OriginPlayerID_all,DesinationPlayerID_all = \
        Matchwise_team_members_get(single_Match_all_info, team_name)
        
        single_member_attract_items = {member:{'catch_ball_time':0, 'pass_all_kind_count':\
                                      {pass_type:0 for pass_type in pass_type_list}} for member in team_members}


        for i in range(len(single_Match_all_info)):
            # 统计传球种类
            info_temp = single_Match_all_info[i]
            origin_player_ID = info_temp['OriginPlayerID']
            dest_player_ID = info_temp['DestinationPlayerID']
            if(team_name not in origin_player_ID):
                continue
            if(team_key_word_extract(origin_player_ID) != team_key_word_extract(dest_player_ID)):
                continue
            # 统计出场 ID
            pass_type = info_temp['EventSubType']
            single_member_attract_items[origin_player_ID]['pass_all_kind_count'][pass_type] += 1
            # 统计带球时间
            if(i == 0):
                continue
            info_1 = single_Match_all_info[i-1]
            info_2 = single_Match_all_info[i]
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
            f.write('持球时间 = {} min\n'.format(single_member_attract_items[member]['catch_ball_time']/60))
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
        f.write('===========================================================================\n')
    f.close()

if(flag_event_coordinate_per_player):
    f = open('{}/{}_coordinate_origin_dest_avg.txt'.format(result_path, team_name), 'w', encoding='utf-8')
    # 'OriginPlayerID', 'DestinationPlayerID'
    # 'EventOrigin_x', 'EventOrigin_y', 'EventDestination_x', 'EventDestination_y'
    for MatchID in MatchID_list:
        f.write('[{}]\n\n'.format(MatchID))

        single_Match_all_info = Matchwise_all_info[MatchID-1]

        team_members,OriginPlayerID_all,DesinationPlayerID_all = \
        Matchwise_team_members_get(single_Match_all_info, team_name)

        origin_team_members = origin_or_dest_team_member_get(OriginPlayerID_all, team_name)
        
        coordinate_per_player = {member:{'origin':[]} for member in origin_team_members}
        coordinate_avg_per_player = {member:{'origin':None} for member in origin_team_members}

        for line in single_Match_all_info:
            origin_player_ID = line['OriginPlayerID']
            if(team_name not in origin_player_ID):
                continue
            origin_x = float(line['EventOrigin_x'])
            origin_y = float(line['EventOrigin_y'])
            coordinate_per_player[origin_player_ID]['origin'].append((origin_x, origin_y))
        
        for member in origin_team_members:
            origin_temp = coordinate_per_player[member]['origin']
            coordinate_avg_per_player[member]['origin'] = (average([x[0] for x in origin_temp]), \
                                                           average([x[1] for x in origin_temp]))    

        f.write('队伍成员传接球站位统计!!\n=========================================================\n')

        for member in origin_team_members:
            f.write('[{}]\n'.format(member))
            f.write('传球平均坐标：x:{} y:{}\n'.format(*coordinate_avg_per_player[member]['origin']))
            f.write('\n')

        f.write('\n')
    f.close()