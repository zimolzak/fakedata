#!/bin/sh

head dist.all.last         > ./sample_datasets/dist.all.last
head dist.female.first     > ./sample_datasets/dist.female.first
head dist.male.first       > ./sample_datasets/dist.male.first
head npanxx99.txt          > ./sample_datasets/npanxx99.txt
head zip_code_database.csv > ./sample_datasets/zip_code_database.csv
head zipcodes.csv          > ./sample_datasets/zipcodes.csv
cp patients.csv ./sample_datasets/
cp labs.csv     ./sample_datasets/
