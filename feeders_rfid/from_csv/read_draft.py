import csv
from collections import defaultdict

columns = defaultdict(list)

fname = 'filename2.csv'
with open(fname) as csvfile:
    reader = csv.DictReader(csvfile)
    # for row in reader:
    #     for (k,v) in row.items():
    #         columns[k].append(v)
    #         # print(columns['TAG'])
    #         tag, antenna = columns['TAG'], columns['ANTENNA']
    #         print (tag)

    for row in reader:
        tag, antenna = row['TAG'], row['ANTENNA']
        # print (row['TAG'])
        print (antenna)

    if antenna == '102':
        print ("yes")