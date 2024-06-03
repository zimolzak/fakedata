#!/usr/bin/env python
# usage: ./fakedata.py
# outputs labs.csv patients.csv
import csv
import random
import datetime
from lab import *
from names import *
from genes import *
from dict_csv_tools import *
# import schema # maybe later
# import json # maybe later

#### Parameters
delta = 0.03 # brownian motion param, units 1/time^2. Hi=labile, lo=stable.
avg_days = 90 # mean days between two lab measurements
labs_per_patient = 20
patients_to_generate = 30

#### Initialize CSV files with headers
labwriter = csv.writer(open('labs.csv', 'w'))
labwriter.writerow(["id", "date"] + list(public(vars(CbcBmp())).keys()))

patientwriter = csv.writer(open('patients.csv', 'w'))
patientwriter.writerow(["id"] + list(public(vars(Patient())).keys()) + list(public(vars(Tumor())).keys()))

#### Generate patients

for id in range(patients_to_generate):
    patientwriter.writerow([id] + list(public(vars(Patient())).values()) \
                               + list(public(vars(Tumor())).values()))

    ### Generate repeated labs over time
    Panel = CbcBmp(star=False)
    t = datetime.date(2014,1,1) + datetime.timedelta(random.randint(0,365))
    for i in range(labs_per_patient):
        labwriter.writerow([id, str(t)] + list(public(vars(Panel)).values()))
        # The update rules are below.
        dt = datetime.timedelta(int(random.expovariate(1.0 / avg_days)))
        t = t + dt
        Panel.update(delta,dt)
