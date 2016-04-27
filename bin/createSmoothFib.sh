offFile=$1
outFib=$2
iStep=$3

step=`echo "$iStep*0.2"|bc -l`
echo $step

scaledFile=${offFile%.off}-s0.2.off
scaledFib=/tmp/scaledFib.xyz

../scaleOFF.sh 0.2 $offFile $scaledFile
../build/TubeAnalyse/tubeAnalyse2 -i $scaledFile -r 40 --computeFiberPatchTrack /tmp/rawfile.xyz -a 0.3 \
--exportOptiFiber $scaledFib -s "$step" \
-n accumulation3.vol --fixRadiusInExportFiberMesh 1 --addSourceMeshExport $scaledFile #--invertNormal

#restore
../scaleXyz.sh 5 $scaledFib Fib.xyz
echo $offFile
echo ../build/Splines -i $offFile -f Fib.xyz -o "$outFib"
../build/Splines -i $offFile -f Fib.xyz -o "$outFib"
