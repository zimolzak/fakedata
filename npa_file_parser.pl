#!/usr/bin/perl -w
use strict;
while(<>){
    chomp;
    s/\r//g;
    my ($npa, $nxx, $lat, $long, $lw, $st, $ci) = split(" ", $_, 7);
    print "$npa,$ci,$st\n"
}
