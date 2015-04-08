#!/bin/sh
# usage ./makepdf.sh
enscript -vGE -o - *.py | ps2pdf - code.pdf
