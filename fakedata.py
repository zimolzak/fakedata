#!/usr/bin/env python
# usage: ./fakedata.py
# outputs labs.csv patients.csv
import csv
import random
import datetime
from lab import *
from names import *
from genes import *
# import schema # maybe later
# import json # maybe later

#### Parameters
delta = 0.03 # brownian motion param, units 1/time^2. Hi=labile, lo=stable.
avg_days = 90 # mean days between two lab measurements
labs_per_patient = 20
patients_to_generate = 30

#### Initialize CSV files with headers
test_panel = CbcBmp()
labwriter = csv.writer(open('labs.csv', 'wb'))
keys_ordered = vars(test_panel).keys()
labwriter.writerow(["id", "date"] + keys_ordered)

test_patient = Patient()
patientwriter = csv.writer(open('patients.csv', 'wb'))
patient_keys_ordered = vars(test_patient).keys()
patientwriter.writerow(["id"] + patient_keys_ordered)

test_tumor = Tumor()
tumorwriter = csv.writer(open('tumor.csv', 'wb'))
tumor_keys_ordered = vars(test_tumor).keys()
tumorwriter.writerow(["id"] + tumor_keys_ordered)

#### Generate patients

for id in range(patients_to_generate):

    ### Initial conditions
    current_person = Patient()
    current_tumor = Tumor()
    Panel = CbcBmp()
    t = datetime.date(2014,1,1) + datetime.timedelta(random.randint(0,365))

    ### Write to patient table
    vals_ordered = []
    for k in patient_keys_ordered:
        vals_ordered.append(current_person.__dict__[k])
    patientwriter.writerow([id] + vals_ordered)

    ### Write to tumor table
    vals_ordered = []
    for k in tumor_keys_ordered:
        vals_ordered.append(current_tumor.__dict__[k])
    tumorwriter.writerow([id] + vals_ordered)

    ### Loop and write to lab table
    for i in range(labs_per_patient):
        vals_ordered = []
        for k in keys_ordered:
            vals_ordered.append(Panel.contents(True)[k])
        labwriter.writerow([id, str(t)] + vals_ordered)
        # The update rules are below.
        dt = datetime.timedelta(int(random.expovariate(1.0 / avg_days)))
        t = t + dt
        Panel.update(delta,dt)
