
def catch_ball_time_calculate(info_1, info_2, member):
    """
    统计单个球员单次接球传球的时间。
    Args:
        info_1,info_2:信息条目。
        member:成员标识名。
    Return:
        bool:该球员是否成功控球。
        time_period:该球员此次控球时间。
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

def team_member_get(OriginPlayerID_all, DestinationPlayerID_all, team_key_word):
    """
    获取某个队伍的球员清单。
    Args:
        OriginPlayerID_all:所有传球队员记录。
        DestinationPlayerID_all:所有接球队员记录。
        team_key_word:球队的关键字。
    Return:
        team_member_list:球队的成员列表，球员一般用 XXteam_XX 表示，'_' 后面的是球员的标识，
        为一个字母和一个数字组合，该列表进行过排序球员首先按字母 D，F，M，G 排序，然后再安装数字排序
    """
    members = []
    for i,j in zip(OriginPlayerID_all, DestinationPlayerID_all):
        # 判断这个球员是否为该队伍。
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
    判断传接球是否是选定方，我方关键词：Husk 敌方关键词：Oppo。
    Args:
        info:判断的数据条目。
    Return:
        bool:是否。
    """
    Origin = info['OriginPlayerID']
    Dest = info['DestinationPlayerID']
    if(team_key_word not in Origin or team_key_word not in Dest):
        return False
    
    return True

def cooperation_detect(info_1, info_2):
    """
    通过输入三个信息条目，来检测是否构成一次配合。
    Args:
        info_1, info_2:两条条目。
    Return:
        players:构成配合的 player_name 列表。
        flag:是否构成配合。
    """
    players = []
    time_accu = 0
    Origin_1 = info_1['OriginPlayerID']
    Origin_2 = info_2['OriginPlayerID']
    Dest_1 = info_1['DestinationPlayerID']
    Dest_2 = info_2['DestinationPlayerID']
    time_stamp_1 = float(info_1['EventTime'])
    time_stamp_2 = float(info_2['EventTime'])
    # 第一次传球与第二次传球判断
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

