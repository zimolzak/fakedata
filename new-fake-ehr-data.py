import csv
import datetime
import random
from names import Patient
from dict_csv_tools import public
from lab import CbcBmp

# Parameters
delta = 0.03  # brownian motion param, units 1/time^2. Hi=labile, lo=stable.
avg_days = 90  # mean days between two lab measurements
labs_per_patient = 20
patients_to_generate = 30

# Initialize CSV files with headers
patient_writer = csv.writer(open('patients-2024.csv', 'w'))
patient_writer.writerow(["id"] + list(public(vars(Patient())).keys()))

lab_writer = csv.writer(open('labs.csv', 'w'))
lab_names = list(public(vars(CbcBmp())).keys())
lab_writer.writerow(["id", "date", "lab_name", "value"])

# Generate patients
for n in range(patients_to_generate):
    patient_writer.writerow([n] + list(public(vars(Patient())).values()))
    lab_obj = CbcBmp(star=False)
    t = datetime.date(2014, 1, 1) + datetime.timedelta(random.randint(0, 365))

    for i in range(labs_per_patient):
        lab_values = list(public(vars(lab_obj)).values())
        for j in range(len(lab_values)):
            lab_writer.writerow([n, str(t), lab_names[j], lab_values[j]])

        # Update the time and the labs.
        dt = datetime.timedelta(int(random.expovariate(1.0 / avg_days)))
        t = t + dt
        lab_obj.update(delta, dt)
