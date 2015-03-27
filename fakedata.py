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
delta = 0.03 # brownian motion param, units 1/time^2. Hi=labile, lo=stable.
avg_days = 90 # mean days between two lab measurements

### Initial conditions
Panel = LabDefinition()
Panel.new_root("na", 136, 145)
Panel.new_root('k', 3.5, 5.0)
Panel.new_root('hco3', 23, 28)
Panel.new_root('bun', 8, 20)
Panel.new_root('cr', 0.7, 1.3)
Panel.new_root('glc', 70, 100)
Panel.new_root('ag', 3, 11)
def cl_func(na, ag, hco3):
    return na - ag - hco3
Panel.new_correlate('cl', cl_func, ['na', 'ag', 'hco3'], how_messy=0)

Panel.new_root("hgb", 12, 17)
Panel.new_root('wbc', 4, 10)
Panel.new_root('plt', 150, 350)
def hgb2hct(hgb):
    return 3 * hgb
Panel.new_correlate('hct', hgb2hct, ['hgb'], how_messy=0.3)

t = datetime.date(2015,1,1)

### Loop and write
labwriter = csv.writer(open('labs.csv', 'wb'))
keys_ordered = Panel.contents().keys()
labwriter.writerow(["date"] + keys_ordered)
for i in range(20):
    vals_ordered = []
    for k in keys_ordered:
        vals_ordered.append(Panel.contents(True)[k])
    labwriter.writerow([str(t)] + vals_ordered)
    # The update rules are below.
    dt = datetime.timedelta(int(random.expovariate(1.0 / avg_days)))
    t = t + dt
    Panel.update(delta,dt)
