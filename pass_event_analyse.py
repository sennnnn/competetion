import os
import csv
import sys

from util import csv_process,team_member_get,team_key_word_extract,cooperation_detect,\
                 catch_ball_time_calculate,average,Matchwise_all_info_get,MatchID_list_get,\
                 Matchwise_team_members_get,origin_or_dest_team_member_get,teamwise_info_get

fullevents_path = 'data/fullevents.csv'
matches_path = 'data/matches.csv'
passingevents_path = 'data/passingevents.csv'

csv_file = csv.reader(open(passingevents_path, 'r'))

all_info = list(csv_file)

team_name = sys.argv[1]

team_list = ['Husk', 'Oppo', 'Opponent1_', 'Opponent2_', 'Opponent3_', 'Opponent4_', \
             'Opponent5_', 'Opponent6_', 'Opponent7_', 'Opponent8_', 'Opponent9_', \
             'Opponent10_', 'Opponent11_', 'Opponent12_', 'Opponent13_', 'Opponent14_', \
             'Opponent15_', 'Opponent16_', 'Opponent17_', 'Opponent18_', 'Opponent19']

# team_name must be one of the team list
assert team_name in team_list, "Error,the first command line arg must be team name and the team name must be \
one of the {}".format(team_name, team_list)

# txt output file save path.
result_path = 'result'

# The save path of all generated file 
if(not os.path.exists(os.path.join('build', team_name, result_path))):
    os.makedirs(os.path.join('build', team_name, result_path), 0x777)

# data item list
# ['MatchID', 'TeamID', 'OriginPlayerID', 'DestinationPlayerID', 'MatchPeriod', 'EventTime', \
# 'EventSubType', 'EventOrigin_x', 'EventOrigin_y', 'EventDestination_x', 'EventDestination_y']

all_info = csv_process(all_info)

# Get informations of the selected teamw.
teamwise_all_info = teamwise_info_get(all_info, team_name)

# Get the match ID that the team has attended.
MatchID_list = MatchID_list_get(teamwise_all_info)

# Get single match information of the selected team.
Matchwise_all_info = Matchwise_all_info_get(teamwise_all_info)

# Parse the command line args.
sys_args = sys.argv[2:]

flag_cooperation_pass = True if('--cp' in sys_args) else False
flag_pass_origin_dest_per_team_member = True if('--pass_memberwise' in sys_args) else False
flag_attractive_force_item_per_team_member = True if('--attractive' in sys_args) else False
flag_event_coordinate_per_player = True if('--coordinate' in sys_args) else False

# 队伍综合能力
# 队伍传球能力：每一场传球次数
# 队伍配合能力：每一场配合次数，二人配合 + 三人配合
# 小队配合能力：二人配合次数，三人配合次数
# 个人配合能力：传球次数，接球次数
if(flag_cooperation_pass):
    team_pass_count = {}
    team_cooperation_count = {}
    team_cooperation_list = {2:[], 3:[]}

    old_MatchID = 0

    for i in range(len(teamwise_all_info)):
        Origin_player_ID = teamwise_all_info[i]['OriginPlayerID']
        Dest_player_ID = teamwise_all_info[i]['DestinationPlayerID']
        MatchID = int(teamwise_all_info[i]['MatchID'])
        if(old_MatchID != MatchID):
            team_pass_count[MatchID] = 0
            team_cooperation_count[MatchID] = {2:0, 3:0}
            team_cooperation_list[MatchID] = {2:[], 3:[]}
            old_MatchID = MatchID
        if(team_name not in Origin_player_ID or team_name not in Dest_player_ID):
            continue
        # 统计传球次数
        team_pass_count[MatchID] += 1
        if(i == 0):
            continue
        # 统计合作次数
        info_1 = teamwise_all_info[i-1]
        info_2 = teamwise_all_info[i]
        players,flag = cooperation_detect(info_1, info_2)
        if(flag):
            team_cooperation_list[MatchID][len(players)].append(tuple(players))
            team_cooperation_count[MatchID][len(players)] += 1

    print(team_pass_count)
    print(team_cooperation_count)
    
    f = open('build/{}/{}/cooperation&pass_count.txt'.format(team_name, result_path), 'w', encoding='utf-8')
    f.write('p.s. 注意 Oppo 是敌队的意思。\n')
    f.write('[传球次数统计] \n比赛场次 | {}队\n'.format(team_name))
    for MatchID in MatchID_list:
        f.write('{}  {}  \n'.format(MatchID, team_pass_count[MatchID]))

    f.write('\n')

    f.write('[配合次数统计] \n比赛场次 | {}队二元配合 | {} 队三元配合\n'\
            .format(team_name, team_name))    
    for MatchID in MatchID_list:
        f.write('{} {} {}\n'.format(MatchID, \
                                    team_cooperation_count[MatchID][2], team_cooperation_count[MatchID][3]))
        
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
    f = open('build/{}/{}/pass_origin.txt'.format(team_name, result_path), 'w', encoding='utf-8')
    f_ = open('build/{}/{}/pass_dest.txt'.format(team_name, result_path), 'w', encoding='utf-8')

    for MatchID in MatchID_list:
        f.write('[{}]\n'.format(MatchID))
        f_.write('[{}]\n'.format(MatchID))
        single_Match_all_info = Matchwise_all_info[MatchID]

        team_members,OriginPlayerID_all,DesinationPlayerID_all = \
        Matchwise_team_members_get(single_Match_all_info, team_name)

        origin_team_members = origin_or_dest_team_member_get(OriginPlayerID_all, team_name)
        dest_team_members = origin_or_dest_team_member_get(DesinationPlayerID_all, team_name)

        # 传球统计
        playerwise_pass_origin_count = {member:{member_:0 for member_ in team_members} for member in origin_team_members}
        # 接球统计
        playerwise_pass_dest_count  = {member:{member_:0 for member_ in team_members} for member in dest_team_members}
        for member_origin in origin_team_members:
            playerwise_pass_origin_count[member_origin]['all'] = 0

        for member_dest in dest_team_members:
            playerwise_pass_dest_count[member_dest]['all'] = 0

        for i,j in zip(OriginPlayerID_all, DesinationPlayerID_all):
            if(team_name not in i or team_name not in j):
                continue

            # 传出
            playerwise_pass_origin_count[i][j] += 1
            playerwise_pass_origin_count[i]['all'] += 1
            # 接到
            playerwise_pass_dest_count[j][i] += 1
            playerwise_pass_dest_count[j]['all'] += 1

        f.write(str(len(origin_team_members)) + '\n')
        f_.write(str(len(dest_team_members)) + '\n')

        for member in origin_team_members:
            member_dict = playerwise_pass_origin_count[member]
            f.write('[{}]\n'.format(member))
            for i in member_dict.keys():
                if(i == 'all'):
                    continue
                f.write('{} {} {}\n'.format(member, i, member_dict[i]))
            f.write('\n')

        for member in dest_team_members:
            member_dict = playerwise_pass_dest_count[member]
            f_.write('[{}]\n'.format(member))
            for i in member_dict.keys():
                if(i == 'all'):
                    continue
                f_.write('{} {} {}\n'.format(member, i, member_dict[i]))
            f_.write('\n')
        

        f.write('\n')
        f_.write('\n')
    f.close()
    f_.close()

if(flag_attractive_force_item_per_team_member):
    f = open('build/{}/{}/attractive_force_item.txt'.format(team_name, result_path), 'w', encoding='utf-8')
    f_ = open('build/{}/{}/extra_info.txt'.format(team_name, result_path), 'w', encoding='utf-8')
    pass_type_list = ['Head pass', 'Simple pass', 'Launch', 'High pass', 'Hand pass', 'Smart pass', 'Cross']

    all_pass_type_count = [0]*len(pass_type_list)
    all_get_type_count = [0]*len(pass_type_list)

    for MatchID in MatchID_list:

        f.write('[{}]\n'.format(MatchID))

        single_Match_all_info = Matchwise_all_info[MatchID]

        team_members,OriginPlayerID_all,DesinationPlayerID_all = \
        Matchwise_team_members_get(single_Match_all_info, team_name)

        origin_team_members = origin_or_dest_team_member_get(OriginPlayerID_all, team_name)

        single_origin_member_attract_items = {member:{'catch_ball_time':0, 'get_count':0, 'pass_count':0, 
        'pass_all_kind_count':{pass_type:0 for pass_type in pass_type_list}, \
        'get_all_kind_count':{pass_type:0 for pass_type in pass_type_list}} for member in origin_team_members}

        for i in range(len(single_Match_all_info)):
            # 统计传球种类
            info_temp = single_Match_all_info[i]
            origin_player_ID = info_temp['OriginPlayerID']
            dest_player_ID = info_temp['DestinationPlayerID']
            if(team_name not in origin_player_ID):
                continue
            if(team_key_word_extract(origin_player_ID) != team_key_word_extract(dest_player_ID)):
                continue
            if(origin_player_ID in origin_team_members):
                single_origin_member_attract_items[origin_player_ID]['pass_count'] += 1
                # 统计传球事件
                pass_type = info_temp['EventSubType']
                single_origin_member_attract_items[origin_player_ID]['pass_all_kind_count'][pass_type] += 1
                # 统计各种传球总数
                all_pass_type_count[pass_type_list.index(pass_type)] += 1
            if(dest_player_ID in origin_team_members):
                single_origin_member_attract_items[dest_player_ID]['get_count'] += 1
                # 统计接球事件
                get_type = info_temp['EventSubType']
                single_origin_member_attract_items[dest_player_ID]['get_all_kind_count'][pass_type] += 1
                # 统计各种接球总数
                all_get_type_count[pass_type_list.index(pass_type)] += 1
            # 统计带球时间
            if(i == 0):
                continue
            info_1 = single_Match_all_info[i-1]
            info_2 = single_Match_all_info[i]
            race_id_1 = info_1['MatchID']
            race_id_2 = info_2['MatchID']
            if(race_id_1 != race_id_2):
                continue
            if(info_1['MatchPeriod'] != info_2['MatchPeriod']):
                continue
            for member in origin_team_members:
                flag,time = catch_ball_time_calculate(info_1, info_2, member)
                if(flag and time > 0):
                    single_origin_member_attract_items[member]["catch_ball_time"] += time

        f.write('%d\n'%(len(origin_team_members)))
        for member in origin_team_members:
            f.write('{} {} {} {} '.format(member, single_origin_member_attract_items[member]['catch_ball_time'], 
                                          single_origin_member_attract_items[member]['get_count'], \
                                          single_origin_member_attract_items[member]['pass_count']))
            temp_pass = single_origin_member_attract_items[member]['pass_all_kind_count']
            temp_get = single_origin_member_attract_items[member]['get_all_kind_count']
            for key in temp_get.keys():
                f.write('{} '.format(temp_get[key]))
            for key in temp_pass.keys():
                f.write('{} '.format(temp_pass[key]))
            f.write('\n')
        f.write('\n')
    f.close()
    f_.write(str(MatchID_list) + '\n')
    f_.write(str(all_pass_type_count) + '\n')
    f_.write(str(all_get_type_count) + '\n')
    print(all_pass_type_count)
    print(all_get_type_count)


if(flag_event_coordinate_per_player):
    f = open('build/{}/{}/coordinate_origin_avg.txt'.format(team_name, result_path), 'w', encoding='utf-8')
    # 'OriginPlayerID', 'DestinationPlayerID'
    # 'EventOrigin_x', 'EventOrigin_y', 'EventDestination_x', 'EventDestination_y'
    for MatchID in MatchID_list:
        f.write('[{}]\n'.format(MatchID))

        single_Match_all_info = Matchwise_all_info[MatchID]

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

        f.write(str(len(origin_team_members)) + '\n')
        for member in origin_team_members:
            f.write('{} {} {}\n'.format(member, *coordinate_avg_per_player[member]['origin']))

        f.write('\n')
    f.close()