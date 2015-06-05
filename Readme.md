Fake Data from Scratch
========================

Andrew Zimolzak, MD, MMSc

Generate structured medical data from "first principles."

Introduction
--------

What should we do when an algorithm, app, data model, etc. needs some
data to practice on? One approach is to take real private health
records and deidentify them, but we don't like this approach because
it's fraught with problems (see below).

Code explanation
---------

Usage:

    ./make_npa_city_state.sh    # needs to be run one time only
    ./fakedata.py
    ./make_sample_datasets.sh
    ./makepdf.sh

Outputs CSV files of demographics + histology + genes, and lab data
(patients.csv, labs.csv).

Input files:

* bmp_ranges.csv (handcrafted)
* cbc_ranges.csv (handcrafted)
* dist.all.last, dist.female.first, dist.male.first
  (http://www2.census.gov/topics/genealogy/1990surnames/dist.male.first)
* npanxx99.txt (honestly not sure where I downloaded this)
* zipcodes.csv (population distribution by zip code, downloaded from
  factfinder.census.gov and manually edited into this form. )
* zip_code_database.csv (used to decode city, state. From
  unitedstateszipcodes.org)
* histology.csv (handcrafted)

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

* Response of cancer to treatment (progressing | stable | remitting)

* More dates: of diagnosis, recruitment, upcoming appointments with
  oncology, rad-onc, chemotherapy.

* vital signs

* What level of consent for Precision Oncology.

* Era of military service.

* consider splitting out one lab per line. (id=0, date=2014-04-04,
  lab=hgb, val=10.2)

* make it messy in deeper ways (messy can mean more than just out of
  range results).

* curl to automate download of 

What does 'fraught' mean?
--------

Here is my argument for why we may want fake data from scratch rather
than deidentified real data.

First: 45 CFR 164.514 describes two ways in which covered entities may
classify information as not individually identifiable. (A.) A person
with knowledge of statistical means for "rendering information not
individually identifiable" must determine that the reidentification
risk "is very small." (B.) The identifiers that 45 CFR specifies must
be removed.

Second: Erika Holmberg’s notes on data security say "MAVERIC has not
previously certified datasets as de-identified."

Third: Because of the first two points, I am not sure that it is
enough to do small tinkering with dates and/or lab values. 

Fourth: Data from scratch is what Vick, Ned, and I thought we would
try to start with, because of all these regulatory and statistical
issues. Ultimately it depends what works for Cytolon.
