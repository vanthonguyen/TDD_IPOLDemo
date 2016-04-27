#!/bin/sh

filename=$2
scale=$1
outfile=$3

first=true
nbPoint=10000000
index=0
skipLines=0
truncate -s 0 "$outfile"
while read -r line
do
    #skip header
    if [ "$line" = "OFF" -o "${line:0:1}" = "#" ]; then
        echo $line >>"$outfile"
        skipLines=$(( skipLines+1 ))
        continue
    fi
    #number of point
    if [ "$first" = true ] ; then
        nbPoint=`echo $line | awk '{print $1}'`
        first=false
        echo $nbPoint
        echo $line >>"$outfile"
        skipLines=$(( skipLines+1 ))
        break
    fi
done < "$filename"
    beforeFaces=$(( nbPoint+skipLines ))
    beginFaces=$(( beforeFaces+1 ))
echo "beforeFaces" $beforeFaces
    head -n $beforeFaces "$filename" |tail -n $nbPoint | awk -v d="$scale" '{printf("%.3f %.3f %.3f\n",$1*d,$2*d,$3*d)}'>>"$outfile"
echo "end awk"
    tail -n+"$beginFaces" "$filename" >>"$outfile"
echo "end"

exit 0
