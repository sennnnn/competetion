import math

def coordinate_info_extract(file_object, MatchID, info_dict):
    file_object.readline()
    while(1):
        line = file_object.readline()
        line = line.strip()
        if(line == '[%d]'%(MatchID)):
            line = file_object.readline().strip()
            length = int(line)
            for i in range(length):
                line = file_object.readline().strip()
                infos = line.split(' ')
                info_dict[infos[0]] = {}
                info_dict[infos[0]]['coordinate'] = (float(infos[1])/100, float(infos[2])/100)
            
            return info_dict

def attractive_force_info_extract(file_object, MatchID, info_dict, catch_kind_weight, pass_kind_weight):
    line = file_object.readline()
    while(1):
        line = file_object.readline()
        line = line.strip()
        if(line == '[%d]'%(MatchID)):
            line = file_object.readline().strip()
            length = int(line)
            for i in range(length):
                line = file_object.readline().strip()
                infos = line.split(' ')
                catch_time = float(infos[1])
                catch_count = int(infos[2])
                pass_count = int(infos[3])
                catch_all_type_list = [int(x)*weight for x,weight in zip(infos[4:11], catch_kind_weight)]
                pass_all_type_list = [int(x)*weight for x,weight in zip(infos[11:], pass_kind_weight)]
                info_dict[infos[0]]['attrc'] = catch_time/60 + sum(catch_all_type_list) + sum(pass_all_type_list)
            
            return info_dict

def edge_info_extract(file_object, MatchID, edge_dict, members_ID):
    edge_count = 0
    while(1):
        line = file_object.readline()
        line = line.strip()
        if(line == '[%d]'%(MatchID)):
            line = file_object.readline().strip()
            length = int(line)
            for i in range(length):
                line = file_object.readline()
                while(1):
                    line = file_object.readline()
                    if(line == '\n'):
                        break
                    line = line.strip()
                    infos = line.split()
                    origin = infos[0]
                    dest = infos[1]
                    number = int(infos[2])
                    if(number == 0 or origin == dest or dest not in members_ID):
                        continue
                    edge_count += 1
                    edge_dict[edge_count] = (number, (members_ID.index(origin), members_ID.index(dest)))
            
            return edge_dict

def pair_clustering_coff_cal(member_index_list, edge_list):
    avg_c_f = 0
    for member_index in member_index_list:
        open_single = 0
        close_single = 0
        first_connect_node = []
        for first_edge in edge_list:
            if(first_edge[0] == member_index):
                first_connect_node.append(first_edge[1])
        for first in first_connect_node:
            for second_edge in edge_list:
                if(second_edge[0] == first):
                    if(second_edge[1] == member_index):
                        close_single += 1
                    else:
                        open_single += 1
        avg_c_f += 2*close_single/(2*close_single + open_single)
    
    return avg_c_f/len(member_index_list)

def clustering_coff_cal(member_index_list, edge_list):
    avg_c_f = 0
    for member_index in member_index_list:
        open_single = 0
        close_single = 0
        first_connect_node = []
        for first_edge in edge_list:
            if(first_edge[0] == member_index):
                first_connect_node.append(first_edge[1])
        for first in first_connect_node:
            second_connect_node = []
            for second_edge in edge_list:
                if(second_edge[0] == first):
                    second_connect_node.append(second_edge[1])
            
            for second in second_connect_node:
                for third_edge in edge_list:
                    if(third_edge[0] == second):
                        if(third_edge[1] == member_index):
                            close_single += 1
                        else:
                            open_single += 1

        avg_c_f += 3*close_single/(3*close_single + open_single)

    return avg_c_f/len(member_index_list)

def distance(point_x, point_y):

    return math.sqrt(((point_x[0] - point_y[0])**2 + (point_x[1] - point_y[1])**2))

def r_coff(x, y):
    avg_x = average(x)
    avg_y = average(y)
    under_x = 0
    under_y = 0
    above = 0
    for i,j in zip(x,y):
        above += (i - avg_x) * (j - avg_y)
        under_x += (i - avg_x)**2
        under_y += (j - avg_y)**2

    return above/(math.sqrt(under_x) * math.sqrt(under_y))

def l2_norm_sum(iter_object):
    temp = 0
    for i in iter_object:
        temp += i**2

    return math.sqrt(temp)


def teamwise_info_get(all_info, team_name):
    ret_info = []
    for line in all_info:
        if(team_name not in line['OriginPlayerID'] or team_name not in line['DestinationPlayerID']):
            continue
        ret_info.append(line)

    return ret_info

def Matchwise_team_members_get(Single_Match_all_info, team_name):
    OriginPlayerID_all = [x['OriginPlayerID'] for x in Single_Match_all_info]
    DesinationPlayerID_all = [x['DestinationPlayerID'] for x in Single_Match_all_info]

    team_members = team_member_get(OriginPlayerID_all, DesinationPlayerID_all, team_name)

    return team_members,OriginPlayerID_all,DesinationPlayerID_all

def MatchID_list_get(all_info):
    ret_list = []
    for line in all_info:
        if(int(line['MatchID']) not in ret_list):
            ret_list.append(int(line['MatchID']))
    
    return ret_list

def Matchwise_all_info_get(all_info):
    ret_dict = {}
    old_Match_ID = 0
    for line in all_info:
        MatchID = int(line['MatchID'])
        if(old_Match_ID != MatchID):
            ret_dict[MatchID] = []
            old_Match_ID = MatchID
        ret_dict[MatchID].append(line)
        
    return ret_dict

def average(iterable_object):
    temp = 0
    sum = 0
    for i in iterable_object:
        sum += i
        temp += 1
    
    return sum/temp

def catch_ball_time_calculate(info_1, info_2, member):
    """
    count single catch ball time.
    Args:
        info_1,info_2:info item
        member:player name
    Return:
        bool:fail to catch ball
        time_period:catch ball time.
    """
    Origin_1 = info_1['OriginPlayerID']
    Origin_2 = info_2['OriginPlayerID']
    Dest_1 = info_1['DestinationPlayerID']
    Dest_2 = info_2['DestinationPlayerID']
    time_stamp_1 = float(info_1['EventTime'])
    time_stamp_2 = float(info_2['EventTime'])
    if(Dest_1 != member or Origin_2 != member):
        return False,0

    return True,time_stamp_2-time_stamp_1

def csv_process(csv_list):
    item_list = csv_list[0]
    ret_list = []
    csv_list = csv_list[1:]
    for one_line in csv_list:
        ret_list.append({x:y for x,y in zip(item_list, one_line)})
    
    return ret_list

def ret_from_player_ID(ID, int_max):
    string = ID.split('_')[1]
    char_1,char_2 = string[0],string[1:]
    temp = 0
    if(char_1 == 'D'):
        temp = 0
    elif(char_1 == 'F'):
        temp = int_max
    elif(char_1 == 'M'):
        temp = int_max*2
    elif(char_1 == 'G'):
        temp = int_max*3
    else:
        temp = int_max*4
    
    return temp + int(char_2)

def origin_or_dest_team_member_get(PlayerID_all, team_key_word):
    members = []
    for i in PlayerID_all:
        if(team_key_word not in i):
            continue
        if(i not in members):
            members.append(i)

    member_count = len(members)
    members = sorted(members, key=lambda x : ret_from_player_ID(x, member_count))

    return members

def team_member_get(OriginPlayerID_all, DestinationPlayerID_all, team_key_word):
    """
    team member list get
    Args:
        OriginPlayerID_all:pass player records 
        DestinationPlayerID_all:catch player records
        team_key_word:key word of the team
    Return:
        team_member_list:sorted member list
    """
    members = []
    for i,j in zip(OriginPlayerID_all, DestinationPlayerID_all):
        if(team_key_word not in i or team_key_word not in j):
            continue
        if(i not in members):
            members.append(i)
        if(j not in members):
            members.append(j)
    
    member_count = len(members)
    members = sorted(members, key=lambda x : ret_from_player_ID(x, member_count))

    return members

def team_key_word_extract(ID):
    return ID.split('_')[0][:4]

def pass_side_judge(info, team_key_word):
    """
    judge the pass side
    Args:
        info:judge info item
    Return:
        bool:True or False
    """
    Origin = info['OriginPlayerID']
    Dest = info['DestinationPlayerID']
    if(team_key_word not in Origin or team_key_word not in Dest):
        return False
    
    return True

def cooperation_detect(info_1, info_2):
    """
    detect if info_1 and info_2 construct a cooperation.
    Args:
        info_1, info_2:info item
    Return:
        players:cooperation player name list
        flag:if constructing a cooperation
    """
    players = []
    time_accu = 0
    Origin_1 = info_1['OriginPlayerID']
    Origin_2 = info_2['OriginPlayerID']
    Dest_1 = info_1['DestinationPlayerID']
    Dest_2 = info_2['DestinationPlayerID']
    time_stamp_1 = float(info_1['EventTime'])
    time_stamp_2 = float(info_2['EventTime'])
    # judge between the first pass and the second pass 
    if((time_stamp_2-time_stamp_1) > 5 or (time_stamp_2-time_stamp_1) < 0):
        return players, False
    else:
        if(team_key_word_extract(Origin_1) != team_key_word_extract(Origin_2)):
            return players, False
        else:
            if(Dest_1 != Origin_2 or Origin_1 == Dest_1 or Origin_2 == Dest_2):
                return players, False
            else:
                players.append(Origin_1)
                players.append(Dest_1)
                players.append(Origin_2)
                players.append(Dest_2)
                temp = list(set(players))
                players = sorted(temp, key=players.index)
                return players, True

