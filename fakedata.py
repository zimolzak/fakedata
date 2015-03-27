#!/usr/bin/env python
# usage: ./fakedata.py
# outputs labs.csv
import csv
import random
import datetime
from lab import *
# import schema # maybe later
# import json # maybe later

#### Parameters
messy = 0.3 # higher means worse correlation.
delta = 0.04 # brownian motion param, units 1/time^2. Hi=labile, lo=stable.
avg_days = 90 # mean days between two lab measurements

### Initial conditions
# cbc = LabDefinition("hgb", 12, 17)
# cbc.new_correlate('hct', hgb2hct, 'hgb', messy) # lambda x: 3*x
# cbc.new_root('wbc', 4, 10)
# cbc.new_root('plt', 150, 350)
BMP = LabDefinition("na", 136, 145)
BMP.new_root('k', 3.5, 5.0)
BMP.new_root('hco3', 23, 28)
BMP.new_root('bun', 8, 20)
BMP.new_root('cr', 0.7, 1.3)
BMP.new_root('glc', 70, 100)
BMP.new_root('ag', 3, 11)

def cl_func(na, ag, hco3):
    return na - ag - hco3

BMP.new_correlate('cl', cl_func, ['na', 'ag', 'hco3'], how_messy=0)

t = datetime.date(2015,1,1)

labwriter = csv.writer(open('labs.csv', 'wb'))
keys_ordered = BMP.contents().keys()
labwriter.writerow(["date"] + keys_ordered)
for i in range(20):
    vals_ordered = []
    for k in keys_ordered:
        vals_ordered.append(BMP.contents(True)[k])
    labwriter.writerow([str(t)] + vals_ordered)
    # The update rules are below.
    dt = datetime.timedelta(int(random.expovariate(1.0 / avg_days)))
    t = t + dt
    BMP.update(delta,dt)
