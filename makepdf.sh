#!/bin/sh
# usage ./makepdf.sh
enscript -vGE -o - fakedata.py | ps2pdf - fakedata.pdf
