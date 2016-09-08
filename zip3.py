## Input a file of population by 5 digit ZIP code. Print population
## summed up by initial 3 digits of the ZIP code.

## 25 sec of CPU time
## python zip3.py > ziptable.csv
## sort -n ziptable.csv | less
## sort -nr ziptable.csv | less

lines = open('zipcodes.csv', 'r').read().splitlines()

zip_txt = map(lambda x: x.split(',')[0], lines)
population = map(lambda x: int(x.split(',')[1]), lines)

def extract_3_digits(field):
    [junk, zip5] = field.split()
    return zip5[0:3]

zip3_set = set(map(extract_3_digits, zip_txt))

h = dict.fromkeys(zip3_set, 0)

for k in h.keys():
    for i, z in enumerate(zip_txt):
        if extract_3_digits(z) == k:
            h[k] += population[i]

for k, v in h.iteritems():
    print str(v) + ',' + k
