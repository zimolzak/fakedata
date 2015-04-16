#!/usr/bin/env python

import random

def binomialvariate(n,p):
    X = 0
    for i in range(n):
        if random.uniform(0,1) < p:
            X = X + 1
    return X

sum = 0
ntrials = 2000
ngenes = 87
average = 3.0
for i in range(ntrials):
    b = binomialvariate(ngenes, (average/ngenes))
    sum = sum + b
    #print b
print "Observed average: " + str(sum / float(ntrials))
print "Expected average: " + str(average)

