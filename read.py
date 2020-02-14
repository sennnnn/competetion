import cv2
import csv

fullevents_path = 'data/fullevents.csv'
matches_path = 'data/matches.csv'
passingevents_path = 'data/passingevents.csv'

csv_file = csv.reader(open(passingevents_path, 'r'))

all_info = list(csv_file)

d = [[] for i in range(len(all_info[0]))]

for i in all_info:
    for index in range(len(i)):
        if(i[index] not in d[index]):
            d[index].append(i[index])

print(d[:4])