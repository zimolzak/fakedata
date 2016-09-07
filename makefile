all : dist.all.last dist.male.first dist.female.first npa_city_state.csv zip_code_database.csv
	./fakedata.py
	./make_sample_datasets.sh
	./makepdf.sh

npa_city_state.csv : npanxx99.txt
	./make_npa_city_state.sh

dist.all.last : 
	curl -O 'https://www2.census.gov/topics/genealogy/1990surnames/dist.all.last'

dist.male.first : 
	curl -O 'https://www2.census.gov/topics/genealogy/1990surnames/dist.male.first'

dist.female.first : 
	curl -O 'https://www2.census.gov/topics/genealogy/1990surnames/dist.female.first'

zip_code_database.csv :
	curl -O 'http://www.unitedstateszipcodes.org/zip_code_database.csv'
