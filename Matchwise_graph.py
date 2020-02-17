import os
import sys
import math

import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from util import distance,average,clustering_coff_cal,pair_clustering_coff_cal,\
                 coordinate_info_extract,attractive_force_info_extract,edge_info_extract

team_name = sys.argv[1]

# the max count of egde revealing in the graph.
edge_num = 1000

team_list = ['Husk', 'Oppo', 'Opponent1_', 'Opponent2_', 'Opponent3_', 'Opponent4_', \
             'Opponent5_', 'Opponent6_', 'Opponent7_', 'Opponent8_', 'Opponent9_', \
             'Opponent10_', 'Opponent11_', 'Opponent12_', 'Opponent13_', 'Opponent14_', \
             'Opponent15_', 'Opponent16_', 'Opponent17_', 'Opponent18_', 'Opponent19']

if(team_name not in team_list and team_name != 'all'):
    assert False, 'Error,unknown team name.\nTeam name must be one of the list: {}'.format(team_list)

if(team_name == 'all'):
    os.system('python all.py')
    exit()

result_path = 'result'

f = open('build/{}/{}/Matchwise_attrct_cal.txt'.format(team_name, \
         result_path), 'w', encoding='utf-8')
f_ = open('build/{}/{}/Matchwise_weight_point.txt'.format(team_name, \
         result_path), 'w', encoding='utf-8')
f_ex = open('build/{}/{}/S_and_path_avg_c_ff_index.txt'.format(team_name, \
         result_path), 'w', encoding='utf-8')

temp_f = open('build/{}/{}/extra_info.txt'.format(team_name, result_path), 'r')
MatchID_list = eval(temp_f.readline().strip())
pass_kind_weight = eval(temp_f.readline().strip())
catch_kind_weight = eval(temp_f.readline().strip())

for MatchID in MatchID_list:
    plt.cla()
    # one Match

    if(not os.path.exists('build/{}/pic'.format(team_name))):
        os.makedirs('build/{}/pic'.format(team_name), 0x777)

    coordinate_txt_path = 'build/{}/{}/coordinate_origin_avg.txt'.format(team_name, result_path)
    attrc_txt_path = 'build/{}/{}/attractive_force_item.txt'.format(team_name, result_path)
    pass_origin_path = 'build/{}/{}/pass_origin.txt'.format(team_name, result_path)

    members_info = {}

    coordinate_info_extract(open(coordinate_txt_path, 'r'), MatchID, members_info)

    members_ID = list(members_info.keys())

    pass_kind_weight = [1/x if x != 0 else 0 for x in pass_kind_weight];pass_kind_sum = sum(pass_kind_weight)
    catch_kind_weight = [1/x if x != 0 else 0 for x in catch_kind_weight];catch_kind_sum = sum(catch_kind_weight)
    pass_kind_weight = [x/pass_kind_sum for x in pass_kind_weight]
    catch_kind_weight = [x/catch_kind_sum for x in catch_kind_weight]

    # pass types : 'Head pass', 'Simple pass', 'Launch', 'High pass', 'Hand pass', 'Smart pass', 'Cross'

    attractive_force_info_extract(open(attrc_txt_path, 'r'), MatchID, members_info, catch_kind_weight, pass_kind_weight)

    # attractive force item save. 
    f.write('[{}]\n'.format(MatchID))
    [f.write('{} {}\n'.format(member, members_info[member]['attrc'])) for member in members_ID]
    f.write('\n')

    # sort by attractive force
    members_ID = sorted(members_ID, key=lambda x: members_info[x]['attrc'], reverse=True)

    #===================== weight point calculation ===================#
    x_y = [members_info[member]['coordinate'] for member in members_ID]
    weight = [members_info[member]['attrc'] for member in members_ID]
    M = sum(weight)
    mixi = sum([xy[0]*m for xy,m in zip(x_y, weight)])
    miyi = sum([xy[1]*m for xy,m in zip(x_y, weight)])
    weight_point = (mixi/M*100, miyi/M*100)
    f_.write('{} {} {}\n'.format(MatchID, *weight_point))
    #===================================================================#

    #===================== node disperation calculation ===================#
    node_distance_list = []
    for i in range(len(members_ID)):
        x = members_info[members_ID[i]]['coordinate'][0]*100
        y = members_info[members_ID[i]]['coordinate'][1]*100
        temp = distance((x,y), weight_point)
        node_distance_list.append(temp)
    
    avg = average(node_distance_list)

    S = [(x - avg)**2 for x in node_distance_list]
    S = math.sqrt(sum(S)/len(node_distance_list))
    #=======================================================================#

    f_ex.write('{} {} '.format(MatchID, S))

    edge_dict = {}

    edge_info_extract(open(pass_origin_path, 'r'), MatchID, edge_dict, members_ID)


    #===================== weighted average length calculation ===================#
    edge_weight = [y[0] for x,y in edge_dict.items()]
    edge_point = [(y[1][0],y[1][1]) for x,y in edge_dict.items()]
    sum_weight = sum(edge_weight)
    weighted_average_length = []
    for w,p in zip(edge_weight, edge_point):
        member_1 = members_ID[p[0]]
        member_2 = members_ID[p[1]]
        point_1 = members_info[member_1]['coordinate']
        point_2 = members_info[member_2]['coordinate']
        dis_point_1_2 = distance(point_1, point_2)
        weighted_average_length.append(2/sum_weight*dis_point_1_2)
    weighted_average_length = sum(weighted_average_length)

    f_ex.write('{} '.format(weighted_average_length))
    #==============================================================================#

    # sort by the weght of the edge.
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

    clustering_coff = clustering_coff_cal(members_ID_sub_index, edge_list_sort)

    pair_clustering_coff = pair_clustering_coff_cal(members_ID_sub_index, edge_list_sort)

    f_ex.write('{} {}\n'.format(clustering_coff, pair_clustering_coff))

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

    ax = plt.gca()
    ax.set_axis_off()
    plt.savefig('build/{}/pic/Match_{}_network.png'.format(team_name, MatchID), transparent=True)