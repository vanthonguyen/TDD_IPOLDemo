offFile=$1
outFib=$2
iStep=$3

dir="/home/vantho/ipol/demo/app/TDD_IPOLDemo/bin/"
step=`echo "$iStep*0.2"|bc -l`
echo $step

scaledFile=${offFile%.off}-s0.2.off
scaledFib=/tmp/scaledFib.xyz

"$dir"scaleOFF.sh 0.2 $offFile $scaledFile
"$dir"tubeAnalyse2 -i $scaledFile -r 40 --computeFiberPatchTrack /tmp/rawfile.xyz -a 0.3 \
--exportOptiFiber $scaledFib -s "$step" \
-n /tmp/accumulation.vol --fixRadiusInExportFiberMesh 1 --addSourceMeshExport $scaledFile #--invertNormal

#restore
"$dir"scaleXyz.sh 5 $scaledFib Fib.xyz
echo $offFile
echo Splines -i $offFile -f Fib.xyz -o "$outFib"
"$dir"Splines -i $offFile -f Fib.xyz -o "$outFib"
