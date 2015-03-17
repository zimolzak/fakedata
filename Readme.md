Fake Data from Scratch
========================

Andrew Zimolzak, MD, MMSc

2015-03-17

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

    ./fakedata.py

Outputs a CSV file of lab data. Fields are: date the lab was
collected, hemoglobin, hematocrit, and a flag to indicate normal
versus abnormal.

Example:

    date,hgb,hct,abnl
    2015-01-01,11.8,38.8, **
    2015-02-20,11.8,39.5, **
    2015-09-26,12.9,37.8,
    2015-10-18,12.8,38.2,
    2016-04-09,14.0,43.0,

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

Future variables to include
--------
* Patient name, clearly denoted as fake: something like Donaldzz
Martinzz, or Anthonyfake Walkerfake.

* Fake contact details such as 315 Pinefake St, Davidsonvillefake MD
  21035. 410-555-0978. anthonyfake.walkerfake@gmail.com.

* Specific diagnosis.

* More dates: of diagnosis, recruitment, upcoming appointments with
  oncology, rad-onc, chemotherapy.

* Names of meds you've received for cancer.

* Which labs: CBC (about 14 numbers), BMP (about 8 numbers).

* What level of consent for Precision Oncology.

* Age.

* Era of military service.
