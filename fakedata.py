#!/usr/bin/env python
# usage: ./fakedata.py
# outputs labs.csv
import csv
import random
import math
import datetime
# import schema # maybe later
# import json # maybe later

def sigfig(x, number_of_figures = 3):
    return str(round(x, number_of_figures - 1 - int(math.log10(abs(x)))))

def fake_normal_lab(range_low, range_high, how_sick = 0):
    # As how_sick increases, that means wider standard dev.
    assert 0 <= how_sick <= 1
    mu = (range_low + range_high) / 2
    sigma = (range_low - range_high) / 2 * (how_sick + 1)
    return random.normalvariate(mu, sigma)

def correlate(x, f, range_low, range_high, how_messy):
    # Takes x, adds a little error to it, and outputs f(x). The last 3
    # arguments determine how to add the error.
    mu = 0
    sigma = (range_high - range_low) / 2 * how_messy
    epsilon = random.normalvariate(mu, sigma)
    return f(x + epsilon)

def star_if_abnormal(x, range_low, range_high):
    if not (range_low <= x <= range_high):
        return " **"
    else:
        return ""

#### Parameters
hlow = 12 # hgb lower limit of normal. To do: check gender.
hhigh = 17
messy = 0.4 # higher means worse correlation.
delta = 0.1 # brownian motion param, units lab/time^2. Hi=labile, lo=stable.
morbidity_const = 0
avg_days = 90 # mean days between two lab measurements
def hgb2hct(hgb):
    return 3 * hgb

#### Initial conditions
hgb = fake_normal_lab(hlow,hhigh,morbidity_const)
t = datetime.date(2015,1,1)

labwriter = csv.writer(open('labs.csv', 'wb'))
labwriter.writerow(["date", "hgb", "hct", "abnl"])
for i in range(20):
    hct = correlate(hgb, hgb2hct, hlow, hhigh, messy)
    labwriter.writerow([str(t), sigfig(hgb), sigfig(hct),
                        star_if_abnormal(hgb, hlow, hhigh)])
    # The update rules are below.
    dt = datetime.timedelta(int(random.expovariate(1.0 / avg_days)))
    t = t + dt
    hgb = hgb + random.normalvariate(0, delta**2 * dt.days)
