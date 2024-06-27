import csv
import datetime
import random
from names import Patient
from dict_csv_tools import public
from lab import CbcBmp
from visits import VisitDiagnoses

# Parameters
delta = 0.03  # brownian motion param, units 1/time^2. Hi=labile, lo=stable.
avg_days = 90  # mean days between two lab measurements
labs_per_patient = 20
patients_to_generate = 30

# Initialize CSV files with headers
patient_writer = csv.writer(open('patients-2024.csv', 'w'))
patient_writer.writerow(["pat_id"] + list(public(vars(Patient())).keys()))

lab_writer = csv.writer(open('labs.csv', 'w'))
lab_names = list(public(vars(CbcBmp())).keys())
lab_writer.writerow(["pat_id", "date", "lab_name", "value"])

vis_writer = open('visits.csv', 'w')
vis_writer.write("pat_id,date,icd,condition\n")

med_writer = open('meds.csv', 'w')
med_writer.write("pat_id,date,med_prescribed\n")

# Generate patients
for pat_id in range(patients_to_generate):
    pat_id += 1

    # Patient
    patient_writer.writerow([pat_id] + list(public(vars(Patient())).values()))
    lab_obj = CbcBmp(star=False)
    t = datetime.date(2014, 1, 1) + datetime.timedelta(random.randint(0, 365))

    # Lab
    for i in range(labs_per_patient):
        lab_values = list(public(vars(lab_obj)).values())
        for j in range(len(lab_values)):
            lab_writer.writerow([pat_id, str(t), lab_names[j], lab_values[j]])
            # Update the time and the labs.
            dt = datetime.timedelta(int(random.expovariate(1.0 / avg_days)))
            t = t + dt
            lab_obj.update(delta, dt)

    # Visits
    n_visits = random.randint(1, 10)
    p = VisitDiagnoses()
    for i in range(n_visits):
        dx_today, meds_today = p.return_one_visit()
        for r in dx_today:
            #                 ID     ,date,icd,condition\n
            vis_writer.write(str(pat_id) + ',' + r + '\n')
        for r in meds_today:
            med_writer.write(str(pat_id) + ',' + r + '\n')
