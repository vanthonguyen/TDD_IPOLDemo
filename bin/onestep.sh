#!/bin/sh
iFile="$1"
output="$2"
outFib="${iFile%.off}-fib.xyz"
bigStep=100
smallStep=25
echo $1
exit
#first time
dir="/home/vantho/ipol/demo/app/TDD_IPOLDemo/bin/"
tempdir="/home/vantho/ipol/demo/app/TDD_IPOLDemo/tmp/"
echo /bin/sh -c "$dir"createSmoothFib.sh "$iFile" "$tempdir$outFib" "$smallStep" 
/bin/sh "$dir"createSmoothFib.sh "$iFile" "$tempdir$outFib" "$smallStep"

if [ -z "$output" ]; then
    output=rsDefect
fi
echo thresholding -i "$iFile" -f "$outFib" -e 100 -a 25 -o "$output"
/bin/sh "$dir"thresholding -i "$iFile" -f "$tempdir$outFib" -e 100 -a 25 -o "$output"

exit 0
