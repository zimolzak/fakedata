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
    def __init__(self, labname, low, high, number_of_figures = 3):
        self.labname=labname
        self.low=low
        self.high=high
        self.set_random_initial(0)
    def set_random_initial(self, how_sick = 0):
        assert 0 <= how_sick <= 1
        mu = (self.low + self.high) / 2
        sigma = (self.low - self.high) / 2 * (how_sick + 1)
        self.value = random.normalvariate(mu, sigma)
        self.correlates = {}
    def update(self, delta, dt):
        # dt is a timedelta object
        self.value = self.value + random.normalvariate(0, delta**2 * dt.days)
    def correlate(self, f, how_messy):
        # Takes x, adds a little error to it, and outputs f(x).
        mu = 0
        sigma = (self.high - self.low) / 2 * how_messy
        epsilon = random.normalvariate(mu, sigma)
        return self.sigfig(f(self.value + epsilon))
    def sigfig(self, x, number_of_figures = 3):
        return str(round(x, number_of_figures - 1 - int(math.log10(abs(x)))))
    def __repr__(self):
        return self.sigfig(self.value)
    def star_if_abnormal(self):
        if not (self.low <= self.value <= self.high):
            return " **"
        else:
            return ""

#### Parameters
hgb = LabDefinition("hgb", 12, 17)

messy = 0.4 # higher means worse correlation.
delta = 0.1 # brownian motion param, units lab/time^2. Hi=labile, lo=stable.
avg_days = 90 # mean days between two lab measurements
def hgb2hct(hgb):
    return 3 * hgb

### Initial conditions
t = datetime.date(2015,1,1)

labwriter = csv.writer(open('labs.csv', 'wb'))
labwriter.writerow(["date", "hgb", "hct", "abnl"])
for i in range(20):
    hct = hgb.correlate(hgb2hct, messy)
    labwriter.writerow([str(t), hgb, hct, hgb.star_if_abnormal()])
    # The update rules are below.
    dt = datetime.timedelta(int(random.expovariate(1.0 / avg_days)))
    t = t + dt
    hgb.update(delta,dt)
