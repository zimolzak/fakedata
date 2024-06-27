import random
import csv


class VisitDiagnoses:
    def __init__(self):
        dxs = csv.reader(open('diagnoses.csv'))
        self.n_conditions = 0
        self.has_conditions = []

        for row in dxs:
            dx_name = row[0]
            prevalence = row[1]
            self.n_conditions += 1
            if random.uniform(0, 1) < float(prevalence):
                self.has_conditions += [1]
            else:
                self.has_conditions += [0]
