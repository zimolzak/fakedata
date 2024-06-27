#!/usr/bin/env python
import random
import datetime


def quantile2text(quantile: float, filename: str, q_column: int, t_column: int, split_text) -> str:
    """Opens a file that has data on the distribution of some patient characteristic, use quantile to look up and
    return a value. We use it for choosing random names, histology, and stage.

    :param quantile: Random number, usually uniformly chosen from 0..1 or 0..100
    :param filename: What CSV or space-delimited file to open
    :param q_column: Which column of the file contains percentile (c.d.f.)
    :param t_column: Which column contains the text we will return
    :param split_text: What delimiter to split lines of the file. (None implies default Python .split())
    :return: A string showing the random value chosen for the characteristic.
    """
    file = open(filename, 'r')
    found_name = ""
    names_to_pick = []
    matching_proportion = 0.0
    cumu_p = 0.0
    while found_name == "":
        fields = file.readline().split(split_text)
        name = fields[t_column]
        if fields[0] != '':  # catch extra newline
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


class Patient:
    def __init__(self):
        proportion_male = 0.4
        age_ranges = [18, 35, 55, 65, 75, 91]
        age_cumu_p = {
            "M": [0.071, 0.306, 0.541, 0.765, 1.1],
            "F": [0.210, 0.667, 0.834, 0.903, 1.1]
        }

        # source: American FactFinder, factfinder.census.gov. Sex by
        # age by veteran status for the civilian population 18 years
        # and over. 2009-2013 american community survey 5-year
        # estimates. ACS_13_5YR_B21001. By census 5-digit ZIP code
        # tabulation area (ZCTA5).

        # Gender ########

        self.gender = ""
        if random.uniform(0, 1) > proportion_male:
            firstname_file = 'dist.female.first'
            self.gender = "F"
        else:
            firstname_file = 'dist.male.first'
            self.gender = "M"

        # Age and DOB ########

        self._age = None
        age_quantile = random.uniform(0, 1)
        for i, cutpoint in enumerate(age_cumu_p[self.gender]):
            if age_quantile > cutpoint:
                continue
            else:
                self._age = random.randint(age_ranges[i],
                                           age_ranges[i + 1] - 1)
                break
        extradays = random.randint(0, 364)
        self.dob = datetime.date.today() - datetime.timedelta(self._age * 365 + extradays)

        # Name ########

        self.fullname = ""
        for filename in (firstname_file, 'dist.all.last'):
            r = random.uniform(0, 90.0)  # names file only covers 90.5% .. Men only to 90.040
            self.fullname += quantile2text(r, filename, 2, 0, None)
            self.fullname += " "
            # q column is 2 (the c.d.f.), and t column is 0 (text)
        self.fullname = self.fullname.rstrip()

        # Address ########

        self.addr =\
            str(random.randint(10, 9999)) + " " \
            + random.choice(["Elm St", "Pine Blvd", "Maple St", "State St", "Main St",
                             "Washington Ave", "Beacon St", "Congress Ave", "2nd Ave",
                             "1st St", "2nd St", "3rd St", "4th St", "5th St", "6th St",
                             "7th St", "8th St",
                             "9th St", "10th St"])
