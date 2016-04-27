#!/bin/sh
iFile="$1"
output="$2"
outFib="${iFile%.off}-fib.xyz"
bigStep=100
smallStep=25
#first time
dir="/home/vantho/ipol/demo/app/TDD_IPOLDemo/bin/"
tempdir="/home/vantho/ipol/demo/app/TDD_IPOLDemo/tmp/"
echo /bin/sh -c "$dir"createSmoothFib.sh "$iFile" "$tempdir$outFib" "$smallStep" 
/bin/sh -c "$dir"createSmoothFib.sh "$iFile" "$tempdir$outFib" "$smallStep"

if [ -z "$output" ]; then
    output=oneStep
fi
echo thresholding -i "$iFile" -f "$outFib" -e 100 -a 25 -o "$output"
/bin/sh -c "$dir"thresholding -i "$iFile" -f "$tempdir$outFib" -e 100 -a 25 -o "$output"

exit 0
