#!/usr/bin/env python
import csv
import random
import math
import datetime
# import schema # maybe later
# import json # maybe later

######## test creating csv ########

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

######## test generating H&H lab, unrelated to above ########

def sigfig(x):
    number_of_figures = 3
    return round (x, number_of_figures - 1 - int(math.log10(x)))

def fake_normal_lab(range_low, range_high, how_sick = 0):
    assert 0 <= how_sick <= 1 # sicker means wider standard dev.
    mu = (range_low + range_high) / 2
    sigma = (range_low - range_high) / 2 * (how_sick + 1)
    return sigfig(random.normalvariate(mu, sigma))

def correlate(x, slope, range_low, range_high, how_messy, intercept=0):
    sigma_x = (range_high - range_low) / 2
    epsilon = random.normalvariate(0, how_messy * sigma_x)
    x = x + epsilon
    return sigfig(slope * x + intercept)

def star_if_abnormal(x, range_low, range_high):
    if not (range_low <= x <= range_high):
        return " **"
    else:
        return ""

hlow = 12 # hgb lower limit of normal. To do: check gender.
hhigh = 17
messy = 0.4 # higher means worse correlation. 0.4 is pretty good.
t = datetime.date(2015,1,1)
delta = 0.1 # brownian motion parameter
morbidity_const = 0

hgb = fake_normal_lab(hlow,hhigh,morbidity_const) # initial condition

print "date\t\thgb\thct"

for i in range(7):
    hct = correlate(hgb, 3, hlow, hhigh, messy)
    print str(t) + "\t" + str(hgb) + "\t" + str(hct) + \
        star_if_abnormal(hgb, hlow, hhigh)

    # update rules
    dt = datetime.timedelta(int(random.expovariate(1.0/90)))
    t = t + dt
    hgb = sigfig(hgb + random.normalvariate(0, delta**2 * dt.days))
