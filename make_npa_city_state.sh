#!/bin/sh

cat npanxx99.txt | perl -ne 'chomp; ($npa, $nxx, $lat, $long, $lw, $st, $ci) = split(" ", $_, 7); print "$npa,$ci,$st\n"'|sort|uniq > npa_city_state.csv
