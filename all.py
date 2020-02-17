import os
import sys

team_name = ['Husk', 'Oppo', 'Opponent1_', 'Opponent2_', 'Opponent3_', 'Opponent4_', 'Opponent5_', 'Opponent6_', 'Opponent7_', 'Opponent8_', 'Opponent9_', 'Opponent10_', 'Opponent11_', 'Opponent12_', 'Opponent13_', 'Opponent14_', 'Opponent15_', 'Opponent16_', 'Opponent17_', 'Opponent18_', 'Opponent19']

for one in team_name:
    os.system('python pass_event_analyse.py {} --cp --pass_memberwise --attractive --coordinate'.format(one))
    os.system('python Matchwise_graph.py {}'.format(one))
