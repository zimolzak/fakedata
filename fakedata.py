#!/usr/bin/env python
import csv
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
