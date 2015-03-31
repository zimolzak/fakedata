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

for file in ["bmp_ranges.csv", "cbc_ranges.csv"]:
    lines = csv.reader(open(file, 'r'), delimiter=',')
    for fields in lines:
        Panel.new_root(fields[0], *map(float,fields[1:]))

def cl_func(na, ag, hco3):
    return na - ag - hco3
def hgb2hct(hgb):
    return 3 * hgb
def mchc_func(hgb, hct):
    return hgb / (hct / 100)
def rbc_func(hct, mcv):
    return 10 * hct / mcv
def mch_func(hgb, rbc):
    return 10 * hgb / rbc
def neut2lymph(neut):
    return random.uniform(0.66,0.72) * (100 - neut)
def mono_func(n,l,e,b):
    m = 100 - n - l - e - b
    if m > 0:
        return m
    else:
        return 0

Panel.new_correlate('cl', cl_func, ['na', 'ag', 'hco3'])
Panel.new_correlate('hct', hgb2hct, ['hgb'], how_messy=0.3)
Panel.new_correlate('rbc', rbc_func, ['hct', 'mcv']) # must be after hct
Panel.new_correlate('mchc', mchc_func, ['hgb', 'hct']) # must be after hct
Panel.new_correlate('mch', mch_func, ['hgb', 'rbc']) # must be after rbc
Panel.new_correlate('lymph', neut2lymph, ['neut'])
Panel.new_correlate('mono', mono_func, ['neut', 'lymph', 'eos', 'baso'])

t = datetime.date(2014,1,1) + datetime.timedelta(random.randint(0,365))

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
