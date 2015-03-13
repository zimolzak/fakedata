#!/usr/bin/env python
import csv
import random
import math
import datetime
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

def three_sigs(x):
    return round (x, 2-int(math.log10(x)))

def fake_normal_lab(range_low, range_high, how_sick = 0):
    assert 0 <= how_sick <= 1
    return three_sigs (
        random.normalvariate((range_low+range_high)/2,
                             (range_low-range_high)/2 * (how_sick +1)
                             )
        )

def correlate(x, slope, range_low, range_high, how_messy, intercept=0):
    sigma_x = (range_high - range_low) / 2
    epsilon = random.normalvariate(0, how_messy * sigma_x)
    x = x + epsilon
    return three_sigs(slope * x + intercept)

hlow = 14 # hgb lower limit of normal
hhigh = 17
messy = 0.4 # higher means worse correlation. 0.4 is pretty good.
date = datetime.date(2015,1,1)
delta = 0.1 # brownian motion parameter
morbidity_const = 0

hgb = fake_normal_lab(hlow,hhigh,morbidity_const) # initial condition

for i in range(7):
    hct = correlate(hgb, 3, hlow, hhigh, messy)
    print "Date: " + str(date) + " Hemoglobin: " + str(hgb) + \
        " Hematocrit: " + str(hct) + " Ratio: " + \
        str(three_sigs(hct / hgb))

    # update rules
    dt = datetime.timedelta(int(random.expovariate(1.0/90)))
    date = date + dt
    hgb = three_sigs(hgb + random.normalvariate(0, delta**2 * dt.days))
