import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

team_name = 'Husk'

result_path = 'result'

MatchID = 1

# one Match

coordinate_txt_path = '{}/{}_coordinate_origin_avg.txt'.format(result_path, team_name)
attrc_txt_path = '{}/{}_attractive_force_item.txt'.format(result_path, team_name)
pass_origin_path = '{}/{}_pass_origin.txt'.format(result_path, team_name)

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

pass_kind_weight = [1/572, 1/8735, 1/212, 1/586, 1/127, 1/73, 1/130];pass_kind_sum = sum(pass_kind_weight)
get_kind_weight = [1/571, 1/8730, 1/211, 1/583, 1/127, 1/73, 1/130];get_kind_sum = sum(get_kind_weight)
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

G = nx.generators.directed.random_k_out_graph(len(members_ID), 3, 0.5)

remove_list = [(x,y) for x,y,i in G.edges]

G.remove_edges_from(remove_list)

edge_list = []

edge_info_list = []

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
                edge_list.append((members_ID.index(origin), members_ID.index(dest)))
                edge_info_list.append(number)
        break

G.add_edges_from(edge_list)

pos = {i:np.array(members_info[members_ID[i]]['coordinate']) for i in range(len(members_ID))}

node_sizes = [100*members_info[members_ID[i]]['attrc'] for i in range(len(members_ID))]

M = G.number_of_edges()

edge_colors = range(2, M+2)
# edge_alphas = [(5 + i) / (M + 4) for i in range(M)]

nodes = nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color='blue')
edges = nx.draw_networkx_edges(G, pos, node_size=node_sizes, arrowstyle='->',
                               arrowsize=5, edge_color=edge_colors,
                               edge_cmap=plt.cm.Blues, width=1)

# set alpha value for each edge
# for i in range(M):
    # edges[i].set_alpha(edge_alphas[i])

# pc = mpl.collections.PatchCollection(edges, cmap=plt.cm.Blues)
# pc.set_array(edge_colors)
# plt.colorbar(pc)

ax = plt.gca()
ax.set_axis_off()
plt.show()