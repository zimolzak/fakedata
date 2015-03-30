#!/usr/bin/env python
import random
import datetime

Proportion_Male = 0.927
Age_ranges = [18, 35, 55, 65, 75, 91]
Age_cumu_p = {"M":[0.071, 0.306, 0.541, 0.765, 1.1], \
                     "F":[0.210, 0.667, 0.834, 0.903, 1.1]}

# source: American FactFinder, factfinder.census.gov

# Sex by age by veteran status for the civilian population 18 years
# and over. 2009-2013 american community survey 5-year estimates.
# ACS_13_5YR_B21001. By census 5-digit ZIP code tabulation area
# (ZCTA5).

gender = ""
if random.uniform(0,1) > Proportion_Male:
    firstname = 'dist.female.first'
    gender = "F"
else:
    firstname = 'dist.male.first'
    gender = "M"

age = None
age_quantile = random.uniform(0,1)
for i, cutpoint in enumerate(Age_cumu_p[gender]):
    if age_quantile > cutpoint:
        continue
    else:
        age = random.randint(Age_ranges[i], Age_ranges[i+1] - 1)
        break

extradays = random.randint(0,364)
dob = datetime.date(2015, 3, 30) - datetime.timedelta(age * 365 + extradays)

full_name = []
for filename in ('dist.all.last', firstname):
    r = random.uniform(0, 90.483)
    file = open(filename, 'r')
    found_name = ""
    names_to_pick = []
    matching_proportion = 0
    while found_name == "":
        fields = file.readline().split()
        name = fields[0]
        [p, cumu_p, rank] = map(float, fields[1:])
        if r <= cumu_p and matching_proportion == 0:
            names_to_pick.append(name)
            matching_proportion = cumu_p
            continue
        elif r <= cumu_p and matching_proportion == cumu_p:
            names_to_pick.append(name)
            continue
        elif r > cumu_p:
            continue
        else:
            assert r <= cumu_p and matching_proportion < cumu_p
            found_name = random.choice(names_to_pick).capitalize()
    full_name.append(found_name)

full_name.append(gender)
full_name.append(age)
full_name.append(dob)
print full_name
