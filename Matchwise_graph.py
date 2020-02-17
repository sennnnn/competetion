import os
import sys
import math

import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from util import distance,average

team_name = sys.argv[1]

edge_num = 10000

if(team_name == 'all'):
    os.system('python all.py')

team_name_list = ['Husk', 'Oppo', 'Opponent1_', 'Opponent2_', 'Opponent3_', 'Opponent4_', 'Opponent5_', 'Opponent6_', 'Opponent7_', 'Opponent8_', 'Opponent9_', 'Opponent10_', 'Opponent11_', 'Opponent12_', 'Opponent13_', 'Opponent14_', 'Opponent15_', 'Opponent16_', 'Opponent17_', 'Opponent18_', 'Opponent19']

if(team_name not in team_name_list and team_name != 'all'):
    print('Error,unknown team name.\nTeam name must be one of the list: {}'.format(team_name_list))
    exit()

result_path = 'result'

f = open('build/{}/{}/Matchwise_attrct_cal.txt'.format(team_name, \
         result_path), 'w', encoding='utf-8')
f_ = open('build/{}/{}/Matchwise_weight_point.txt'.format(team_name, \
         result_path), 'w', encoding='utf-8')
f_ex = open('build/{}/{}/S_and_path_avg_index.txt'.format(team_name, \
         result_path), 'w', encoding='utf-8')

temp_f = open('build/{}/{}/extra_info.txt'.format(team_name, result_path), 'r')
MatchID_list = eval(temp_f.readline().strip())
pass_kind_weight = eval(temp_f.readline().strip())
get_kind_weight = eval(temp_f.readline().strip())

for MatchID in MatchID_list:
    plt.cla()
    # one Match

    if(not os.path.exists('build/{}/pic'.format(team_name))):
        os.makedirs('build/{}/pic'.format(team_name), 0x777)

    coordinate_txt_path = 'build/{}/{}/coordinate_origin_avg.txt'.format(team_name, result_path)
    attrc_txt_path = 'build/{}/{}/attractive_force_item.txt'.format(team_name, result_path)
    pass_origin_path = 'build/{}/{}/pass_origin.txt'.format(team_name, result_path)

    f_1 = open(coordinate_txt_path, 'r')
    f_2 = open(attrc_txt_path, 'r')
    f_3 = open(pass_origin_path)

    members_info = {}

    while(1):
        line = f_1.readline()
        line = line.strip()
        if(line == '[%d]'%(MatchID)):
            line = f_1.readline().strip()
            length = int(line)
            for i in range(length):
                line = f_1.readline().strip()
                infos = line.split(' ')
                members_info[infos[0]] = {}
                members_info[infos[0]]['coordinate'] = (float(infos[1])/100, float(infos[2])/100)
            break

    members_ID = list(members_info.keys())

    pass_kind_weight = [1/x if x != 0 else 0 for x in pass_kind_weight];pass_kind_sum = sum(pass_kind_weight)
    get_kind_weight = [1/x if x != 0 else 0 for x in get_kind_weight];get_kind_sum = sum(get_kind_weight)
    pass_kind_weight = [x/pass_kind_sum for x in pass_kind_weight]
    get_kind_weight = [x/get_kind_sum for x in get_kind_weight]

    pass_type_list = ['Head pass', 'Simple pass', 'Launch', 'High pass', 'Hand pass', 'Smart pass', 'Cross']

    while(1):
        line = f_2.readline()
        line = line.strip()
        if(line == '[%d]'%(MatchID)):
            line = f_2.readline().strip()
            length = int(line)
            for i in range(length):
                line = f_2.readline().strip()
                infos = line.split(' ')
                catch_time = float(infos[1])
                get_count = int(infos[2])
                pass_count = int(infos[3])
                get_all_type_list = [int(x)*weight for x,weight in zip(infos[4:11], get_kind_weight)]
                pass_all_type_list = [int(x)*weight for x,weight in zip(infos[11:], pass_kind_weight)]
                members_info[infos[0]]['attrc'] = catch_time/60 + sum(get_all_type_list) + sum(pass_all_type_list)
            break

    # 吸引力计算
    f.write('[{}]\n'.format(MatchID))
    [f.write('{} {}\n'.format(member, members_info[member]['attrc'])) for member in members_ID]
    f.write('\n')

    #  球员按吸引力排序
    members_ID = sorted(members_ID, key=lambda x: members_info[x]['attrc'], reverse=True)

    # 质心计算
    x_y = [members_info[member]['coordinate'] for member in members_ID]
    weight = [members_info[member]['attrc'] for member in members_ID]
    M = sum(weight)
    mixi = sum([xy[0]*m for xy,m in zip(x_y, weight)])
    miyi = sum([xy[1]*m for xy,m in zip(x_y, weight)])
    weight_point = (mixi/M*100, miyi/M*100)
    f_.write('{} {} {}\n'.format(MatchID, *weight_point))

    # 结点离散程度计算
    S = average([distance((members_info[members_ID[i]]['coordinate'][0]*100, members_info[members_ID[i]]['coordinate'][1]*100), weight_point) for i in range(len(members_ID))])

    f_ex.write('{} {} '.format(MatchID, S))

    edge_dict = {}

    edge_info_dict = {}

    edge_count = 0

    while(1):
        line = f_3.readline()
        line = line.strip()
        if(line == '[%d]'%(MatchID)):
            line = f_3.readline().strip()
            length = int(line)
            for i in range(length):
                line = f_3.readline()
                while(1):
                    line = f_3.readline()
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
            break

    # 加权路径长度
    # edge_with_weight = [x,y for x,y in edge_dict.items()]
    edge_weight = [y[0] for x,y in edge_dict.items()]
    edge_point = [(y[1][0],y[1][1]) for x,y in edge_dict.items()]

    weight_length = sum([w/max(edge_weight)*distance(members_info[members_ID[p[0]]]['coordinate'], members_info[members_ID[p[1]]]['coordinate']) for w,p in zip(edge_weight, edge_point)])

    f_ex.write('{} \n'.format(weight_length))

    # 和由边的权重来排序边列表
    edge_list_weight = [edge_dict[key] for key in edge_dict.keys()] 

    edge_list_weight_sort = sorted(edge_list_weight, key=lambda x: x[0], reverse=True)

    edge_list_sort = [x[1] for x in edge_list_weight_sort]

    edge_info_list = [x[0] for x in edge_list_weight_sort]

    edge_list_sub = edge_list_sort[:edge_num]

    edge_info_list_sub = edge_info_list[:edge_num]

    members_ID_sub_index = []
    for edge in edge_list_sub:
        if(edge[0] not in members_ID_sub_index):
            members_ID_sub_index.append(edge[0])
        if(edge[1] not in members_ID_sub_index):
            members_ID_sub_index.append(edge[1])
    members_ID_sub_index = sorted(members_ID_sub_index, key=lambda x: x)
    members_ID_sub = [members_ID[x] for x in members_ID_sub_index]

    G = nx.generators.directed.random_k_out_graph(len(members_ID), 3, 0.5)

    remove_list = [(x,y) for x,y,i in G.edges]

    G.remove_edges_from(remove_list)

    G.add_edges_from(edge_list_sub)

    pos = {i:np.array(members_info[members_ID[i]]['coordinate']) for i in range(len(members_ID))}

    attrc_list = [members_info[members_ID[i]]['attrc'] for i in range(len(members_ID))]

    node_sizes = [500*attrc_list[i]/max(attrc_list) if(members_ID[i] in members_ID_sub) else 0 for i in range(len(attrc_list))]

    M = G.number_of_edges()

    edge_colors = [300 for x in edge_info_list_sub]
    
    edge_info_list_one_normal = [1*(x/sum(edge_info_list_sub)) for x in edge_info_list_sub]

    edge_alphas = [0.6*x/max(edge_info_list_one_normal) for x in edge_info_list_one_normal]

    nodes = nx.draw_networkx_nodes(G, pos, cmap=plt.cm.Blues , node_size=node_sizes)
    edges = nx.draw_networkx_edges(G, pos, node_size=node_sizes, arrowstyle='->',
                                arrowsize=8, edge_color=edge_colors, width=1)
    labels = nx.draw_networkx_labels(G, pos, {i:members_ID[i].split('_')[1] if(members_ID[i] in members_ID_sub) else '' for i in range(len(members_ID))})

    # set alpha value for each edge
    for i in range(M):
        edges[i].set_alpha(edge_alphas[i])

    # pc = mpl.collections.PatchCollection(edges, cmap=plt.cm.Blues)
    # pc.set_array(edge_colors)
    # plt.colorbar(pc)
    ax = plt.gca()
    ax.set_axis_off()
    # plt.show()
    plt.savefig('build/{}/pic/Match_{}_network.png'.format(team_name, MatchID), transparent=True)