#!/usr/bin/env python
# usage: ./fakedata.py
# outputs labs.csv
import csv
import random
import math
import datetime
# import schema # maybe later
# import json # maybe later

class LabDefinition:
    def __init__(self, labname, low, high):
        self.roots = {}
        self.new_root(labname, low, high)
        self.correlate_values = {}
        self.correlate_functions = {}
    def reset_root(self, rootname, how_sick = 0): #may want this public
        assert 0 <= how_sick <= 1
        mu = (self.roots[rootname]['low'] + self.roots[rootname]['high']) / 2
        sigma = (self.roots[rootname]['low'] - self.roots[rootname]['high']) \
            / 2 * (how_sick + 1)
        self.roots[rootname]['value'] = random.normalvariate(mu, sigma)
    def update(self, delta, dt): # definite public
        # dt is a timedelta object
        for k in self.roots.keys():
            midpoint = (self.roots[k]['low'] + self.roots[k]['high']) / 2
            self.roots[k]['value'] = self.roots[k]['value'] + \
                random.normalvariate(0, midpoint * delta**2 * dt.days)
        for k in self.correlate_functions.keys():
            self.reset_correlate(k)
    def new_correlate(self, name, f, rootname, how_messy): # definite public
        self.correlate_functions[name] = \
            {'function':f, 'rootname':rootname, 'messy':how_messy}
        self.reset_correlate(name)
    def reset_correlate(self, name):
        # Takes main value, adds a little error to it, and stores f(x).
        mu = 0
        f = self.correlate_functions[name]['function']
        how_messy = self.correlate_functions[name]['messy']
        myroot = self.correlate_functions[name]['rootname']
        sigma = (self.roots[myroot]['high'] - self.roots[myroot]['low']) \
            / 2 * how_messy
        epsilon = random.normalvariate(mu, sigma)
        self.correlate_values[name] = f(self.roots[myroot]['value'] + epsilon)
    def new_root(self, name, low, high): # definite public
        self.roots[name] = {'low':low, 'high':high}
        self.reset_root(name)
    def sigfig(self, x, number_of_figures = 3):
        return str(round(x, number_of_figures - 1 - int(math.log10(abs(x)))))
    def contents(self, star = False): # definite public
        output = {}
        if star:
            for k, v in self.roots.iteritems():
                output[k] = self.sigfig(v['value']) + self.star_if_abnormal(k)
        else:
            for k, v in self.roots.iteritems():
                output[k] = self.sigfig(v['value'])
        for k, v in self.correlate_values.iteritems():
            output[k] = self.sigfig(v)
        return output
    def star_if_abnormal(self, rootname):
        if not (self.roots[rootname]['low'] \
                    <= self.roots[rootname]['value'] \
                    <= self.roots[rootname]['high']):
            return " **"
        else:
            return ""

#### Parameters
messy = 0.3 # higher means worse correlation.
delta = 0.04 # brownian motion param, units 1/time^2. Hi=labile, lo=stable.
avg_days = 90 # mean days between two lab measurements
def hgb2hct(hgb):
    return 3 * hgb

### Initial conditions
cbc = LabDefinition("hgb", 12, 17)
cbc.new_correlate('hct', hgb2hct, 'hgb', messy)
cbc.new_root('wbc', 4, 10)
cbc.new_root('plt', 150, 350)
t = datetime.date(2015,1,1)

labwriter = csv.writer(open('labs.csv', 'wb'))
keys_ordered = cbc.contents().keys()
labwriter.writerow(["date"] + keys_ordered)
for i in range(20):
    vals_ordered = []
    for k in keys_ordered:
        vals_ordered.append(cbc.contents(True)[k])
    labwriter.writerow([str(t)] + vals_ordered)
    # The update rules are below.
    dt = datetime.timedelta(int(random.expovariate(1.0 / avg_days)))
    t = t + dt
    cbc.update(delta,dt)
