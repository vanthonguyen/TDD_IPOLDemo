#!/bin/sh
while getopts i:o opt; do
  case $opt in
    i)
        iFile=$OPTARG
      ;;
    o)
        output=$OPTARG
      ;;
      exit;
      ;;
  esac
done

shift $(( OPTIND - 1 ));

outFib="${iFile%.off}-fib.xyz"
bigStep=100
smallStep=25
#first time
dir="/home/vantho/ipol/demo/app/TDD_IPOLDemo/bin/"
/bin/sh "$dir"createSmoothFib.sh "$iFile" "$outFib" "$smallStep"

if [ -z "$output" ]; then
    output=oneStep
fi
echo thresholding -i "$iFile" -f "$outFib" -e 100 -a 25 -o "$output"
/bin/sh "$dir"thresholding -i "$iFile" -f "$outFib" -e 100 -a 25 -o "$output"

exit 0
