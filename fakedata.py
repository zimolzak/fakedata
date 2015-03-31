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

bmp_lines = csv.reader(open("bmp_ranges.csv", 'r'),
                       delimiter=',', quotechar='"')
for fields in bmp_lines:
    Panel.new_root(fields[0], *map(float,fields[1:]))
def cl_func(na, ag, hco3):
    return na - ag - hco3
Panel.new_correlate('cl', cl_func, ['na', 'ag', 'hco3'])

Panel.new_root("hgb", None, 12, 17, None)
Panel.new_root('wbc', None, 4, 10, None)
Panel.new_root('plt', None, 150, 350, None)
def hgb2hct(hgb):
    return 3 * hgb
Panel.new_correlate('hct', hgb2hct, ['hgb'], how_messy=0.3)
def mchc_func(hgb, hct):
    return hgb / (hct / 100)
Panel.new_correlate('mchc', mchc_func, ['hgb', 'hct'])
Panel.new_root('mcv', None, 80, 100, None)
def rbc_func(hct, mcv):
    return 10 * hct / mcv
Panel.new_correlate('rbc', rbc_func, ['hct', 'mcv'])
def mch_func(hgb, rbc):
    return 10 * hgb / rbc
Panel.new_correlate('mch', mch_func, ['hgb', 'rbc'])

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
