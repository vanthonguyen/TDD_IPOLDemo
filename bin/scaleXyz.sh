#!/bin/sh
filename=$2
scale=$1
outfile=$3

awk -v d="$scale" '{printf("%.3f %.3f %.3f\n",$1*d,$2*d,$3*d)}' $filename >$outfile

exit 0
