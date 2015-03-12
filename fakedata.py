#!/usr/bin/env python
import csv
import random
# import schema # maybe later
# import json # maybe later
ncols = 6
with open('eggs.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile)
    header =[]
    for i in range(1,ncols+1):
        header.append('col'+str(i))
    spamwriter.writerow(header)
    spamwriter.writerow(['Spam']*5 + ['Baked Beans'])
    spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam',
                         'My parents, Ayn Rand and God', 'foo', 'bar'])

for i in range(7):
    print "Hemoglobin: " +\
        str(round(random.normalvariate((14+17)/2,(14-17)/2),1))

def fake_normal_lab(range_low, range_high, how_sick = 0):
    return random.normalvariate((range_low+range_high)/2,
                                (range_low-range_high)/2 * (how_sick +1)
                                 )
