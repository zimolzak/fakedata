Fake Data from Scratch
========================

Andrew Zimolzak, MD, MMSc

Generate structured medical data from "first principles."

Introduction
--------

What shoud we do when an algorithm, app, data model, etc. needs some
data to practice on? One approach is to take real private health
records and deidentify them, but we don't like this approach because
it's fraught with problems.

Code explanation
---------

Usage:

    ./make_npa_city_state.sh    # needs to be run one time only
    ./fakedata.py

Outputs CSV files of lab data, histology+genes, and demographics
(labs.csv, patients.csv, tumor.csv).

Input files:

* bmp_ranges.csv
* cbc_ranges.csv
* dist.all.last, dist.female.first, dist.male.first
* npanxx99.txt
* zipcodes.csv (population distribution by zip code, calc from census)
* zip_code_database.csv (decode city, state. From
  unitedstateszipcodes.org)
* histology.csv

Current features
--------

* Given the reference range for a lab, code will generate values that
  are usually within this range (for healthy patients) or less likely
  to be within this range (for sick patients).

* Code can handle equations that model relationships between labs. For
  example, hematocrit = hemoglobin * 3. It will also add some
  "fuzziness" to any specified equation.

* Code generates repeated labs for the same patient, at random
  intervals, where "random" is defined in a realistic way. In detail,
  the distribution of intervals between labs follows the exponential
  distribution (somewhat like real life). This is another way of
  saying that the number of lab measurements per unit time follows the
  Poisson distribution.

* Code understands that today's lab is affected by the previous lab
  and how much time has passed since then. In detail, the trend of
  labs over time is modeled as Brownian motion.

* Patient name. First and last names reflect the true distribution of
  names in the US. (But not the joint distribution of first+last, so
  you can get some ethnically unlikely first+last name pairs like
  Ahmed Krzyzewski.)

* Fake contact details such as 315 Pine St, Davidsonville MD 21035.
  410-555-0978. ZIP code of residence simulates the real population
  distribution of the US (all citizens, not just veterans). ZIP is
  decoded to a real city name. Area code is often correct to the level
  of city; always correct by state.

* Which labs: CBC (currently 8 numbers), BMP (about 8 numbers),
  Calcium, WBC differential.

* Age, gender. These two variables simulate the *joint* probability
  distribution of age & gender in US veterans. 

* limits on Brownian motion so it can't get absurd or negative
  numbers, K of 25, Hct of 109, etc.

* Clearly denotes the demographics as fake.

* Genes

* Specific diagnosis (really only histology).

To do
--------

* Names of meds you've received for cancer. What types of meds (oral,
  IV, targeted, traditional). For oral: fill dates & quantities. Other
  CA treatments (surg, rads)?

* Social security number

* Stage of cancer (kinda required in order to pick a random treatment)

Lower priority to do
--------

* Refactor to get more unified way to output CSV, fix up the lab.py
  data structure. That is, simplify the __dict__ of objects of class
  CbcBmp, so we don't have to use the contents() method.

* Response of cancer to treatment (progressing | stable | remitting)

* More dates: of diagnosis, recruitment, upcoming appointments with
  oncology, rad-onc, chemotherapy.

* vital signs

* What level of consent for Precision Oncology.

* Era of military service.
