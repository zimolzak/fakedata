#!/usr/bin/env python
import random
import datetime
import csv

class Patient:
    def __init__(self):
        Proportion_male = 0.927
        Age_ranges = [18, 35, 55, 65, 75, 91]
        Age_cumu_p = {"M":[0.071, 0.306, 0.541, 0.765, 1.1], \
                               "F":[0.210, 0.667, 0.834, 0.903, 1.1]}

        # source: American FactFinder, factfinder.census.gov. Sex by
        # age by veteran status for the civilian population 18 years
        # and over. 2009-2013 american community survey 5-year
        # estimates. ACS_13_5YR_B21001. By census 5-digit ZIP code
        # tabulation area (ZCTA5).
        
        ######## Gender ########
        
        self.gender = ""
        if random.uniform(0,1) > Proportion_male:
            firstname_file = 'dist.female.first'
            self.gender = "F"
        else:
            firstname_file = 'dist.male.first'
            self.gender = "M"

        ######## Age and DOB ########
        
        self.age = None
        age_quantile = random.uniform(0,1)
        for i, cutpoint in enumerate(Age_cumu_p[self.gender]):
            if age_quantile > cutpoint:
                continue
            else:
                self.age = random.randint(Age_ranges[i],
                                          Age_ranges[i+1] - 1)
                break
        extradays = random.randint(0,364)
        self.dob = datetime.date(2015, 3, 30) - \
            datetime.timedelta(self.age * 365 + extradays)

        ######## Name ########
        
        def quantile2text(quantile, filename, q_column, t_column, split_text):
            file = open(filename, 'r')
            found_name = ""
            names_to_pick = []
            matching_proportion = 0
            while found_name == "":
                fields = file.readline().split(split_text)
                name = fields[t_column]
                cumu_p = float(fields[q_column])
                if quantile <= cumu_p and matching_proportion == 0:
                    names_to_pick.append(name)
                    matching_proportion = cumu_p
                    continue
                elif quantile <= cumu_p and matching_proportion == cumu_p:
                    names_to_pick.append(name)
                    continue
                elif quantile > cumu_p:
                    continue
                else:
                    assert quantile <= cumu_p and matching_proportion < cumu_p
                    found_name = random.choice(names_to_pick).capitalize()
            return found_name

        self.fullname = []
        for filename in ('dist.all.last', firstname_file):
            r = random.uniform(0, 90.483)
            self.fullname.append(quantile2text(r, filename, 2, 0, None) \
                                     + "_fake")

        ######## ZIP, City, State ########
        
        self.zip = quantile2text(random.uniform(0,1),
                                 'zipcodes.csv', 2, 0, ",").split()[1]
        # source: http://www.unitedstateszipcodes.org/zip-code-database/

        zipcode_iterator = csv.reader(open("zip_code_database.csv", 'r'),
                                      delimiter=',', quotechar='"')

        self.city = ""
        self.state = ""
        for fields in zipcode_iterator:
            if self.zip != fields[0]:
                continue
            else:
                self.city = fields[2]
                self.state = fields[5]
                break

        ######## Address ########
        
        self.addr = str(random.randint(10,9999)) + " " + \
            random.choice(["Elm", "Pine", "Maple", "State", "Main"]) + " " + \
            random.choice(["St", "Ln", "Blvd"])

        ######## Phone ########
        
        self.phone = ""
        fallback_npa = ""
        npa_iterator = csv.reader(open("npa_city_state.csv", 'r'),
                                  delimiter=',', quotechar='"')
        for npa, test_city, test_state in npa_iterator:
            if test_state == self.state:
                fallback_npa = str(npa)
            if test_state == self.state and test_city == self.city:
                self.phone = str(npa) + "-555-" + str(random.randint(0,9)) \
                    + str(random.randint(0,9)) + str(random.randint(0,9)) \
                    + str(random.randint(0,9))
                break
        if self.phone == "":
            self.phone = fallback_npa + "-555-" + str(random.randint(0,9)) \
                + str(random.randint(0,9)) + str(random.randint(0,9)) \
                + str(random.randint(0,9))

# demographics.append(self.gender)
# demographics.append(self.age)
# demographics.append(self.dob)
# demographics.append(addr)
# demographics.append(city)
# demographics.append(state)
# demographics.append(zip)
# demographics.append(phone)
# print demographics
