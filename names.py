#!/usr/bin/env python
import random

Proportion_Male = 0.8
if random.uniform(0,1) > Proportion_Male:
    firstname = 'dist.female.first'
    gender = "F"
else:
    firstname = 'dist.male.first'
    gender = "M"

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
print full_name
