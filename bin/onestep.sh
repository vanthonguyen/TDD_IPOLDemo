iFile="$1"
output="$2"
outFib="${iFile%.off}-fib.xyz"
bigStep=100
smallStep=25
#first time
../createSmoothFib.sh "$iFile" "$outFib" "$smallStep"

suff="-noerror.off"
if [ -z "$output" ]; then
    output=oneStep
fi
echo ../build/thresholding -i "$iFile" -f "$outFib" -e 100 -a 25 -o "$output"
../build/thresholding -i "$iFile" -f "$outFib" -e 100 -a 25 -o "$output"
