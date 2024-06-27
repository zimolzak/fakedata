import random
import csv
import datetime


class VisitDiagnoses:
    def __init__(self):
        dxs = csv.reader(open('diagnoses.csv'))

        # Blank vars
        self.n_conditions = 0
        self.has_conditions = []
        self.conditions = []
        self.poss_icd = []
        self.poss_med = []
        self.now = datetime.datetime(2014, 1, 1)

        # Read the CSV into blank vars
        for row in dxs:
            dx_name, prevalence, icd1, icd2, m1, m2, m3 = row
            self.n_conditions += 1
            self.conditions += [dx_name]
            self.poss_icd += [[icd1, icd2]]
            self.poss_med += [[m1, m2, m3]]
            if random.uniform(0, 1) < float(prevalence):
                self.has_conditions += [1]
            else:
                self.has_conditions += [0]

    def return_one_visit(self):
        self.now += datetime.timedelta(90) + datetime.timedelta(random.randint(0, 275))
        visit_dx_rows = []  # date, icd, condition
        med_rows = []  # date, med

        for i, pt_has_it in enumerate(self.has_conditions):
            if pt_has_it and random.uniform(0, 1) < 0.75:
                dx_code_str = random.choice(self.poss_icd[i])
                dx_cond_str = self.conditions[i]
                med_str = random.choice(self.poss_med[i])
                visit_dx_rows += [str(self.now) + "," + dx_code_str + "," + dx_cond_str]
                if len(med_str) > 0:
                    med_rows += [str(self.now) + "," + med_str]

        return visit_dx_rows, med_rows
