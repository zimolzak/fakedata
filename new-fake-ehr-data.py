import csv
from names import Patient
from dict_csv_tools import public

# Parameters
delta = 0.03  # brownian motion param, units 1/time^2. Hi=labile, lo=stable.
avg_days = 90  # mean days between two lab measurements
labs_per_patient = 20
patients_to_generate = 30

# Initialize CSV files with headers
patientwriter = csv.writer(open('patients-2024.csv', 'w'))
patientwriter.writerow(["id"] + list(public(vars(Patient())).keys()))

# Generate patients
for id in range(patients_to_generate):
    patientwriter.writerow([id] + list(public(vars(Patient())).values()))
