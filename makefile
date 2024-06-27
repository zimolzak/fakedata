patients-2024.csv labs.csv : dist.all.last dist.male.first dist.female.first \
			npa_city_state.csv zip_code_database.csv \
			new-fake-ehr-data.py names.py dict_csv_tools.py lab.py
	python new-fake-ehr-data.py

all : labs.csv patients-2024.csv sample code.pdf

code.pdf :
	enscript -vGE -o - *.py | ps2pdf - code.pdf

sample : dist.all.last dist.male.first dist.female.first npa_city_state.csv \
	 zip_code_database.csv npanxx99.txt patients.csv labs.csv
	mkdir -p sample_datasets
	head dist.all.last         > ./sample_datasets/dist.all.last
	head dist.female.first     > ./sample_datasets/dist.female.first
	head dist.male.first       > ./sample_datasets/dist.male.first
	head npanxx99.txt          > ./sample_datasets/npanxx99.txt
	head zip_code_database.csv > ./sample_datasets/zip_code_database.csv
	head patients.csv          > ./sample_datasets/patients.csv
	head labs.csv              > ./sample_datasets/labs.csv

npa_city_state.csv : npanxx99.txt
	cat npanxx99.txt | perl -w npa_file_parser.pl | sort | uniq > npa_city_state.csv

dist.all.last : 
	curl -O 'https://www2.census.gov/topics/genealogy/1990surnames/dist.all.last'

dist.male.first : 
	curl -O 'https://www2.census.gov/topics/genealogy/1990surnames/dist.male.first'

dist.female.first : 
	curl -O 'https://www2.census.gov/topics/genealogy/1990surnames/dist.female.first'

zip_code_database.csv :
	curl -O 'http://www.unitedstateszipcodes.org/zip_code_database.csv'

clean :
	rm -f npa_city_state.csv
	rm -f labs.csv
	rm -f patients.csv
	rm -rf sample_datasets
	rm -f code.pdf

cleanall : clean
	rm -f dist.all.last
	rm -f dist.male.first
	rm -f dist.female.first
	rm -f zip_code_database.csv
