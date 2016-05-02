#!/bin/sh

offFile=$1
outFib=$2
iStep=$3
echo $1

step=`echo "$iStep*0.2"|/usr/bin/bc -l`

scaledFile=${offFile%.off}-s0.2.off
scaledFib=scaledFib.xyz

scaleOFF.sh 0.2 $offFile $scaledFile
tubeAnalyse2 -i $scaledFile -r 40 --computeFiberPatchTrack rawfile.xyz -a 0.3 \
--exportOptiFiber $scaledFib -s "$step" \
-n accumulation.vol --fixRadiusInExportFiberMesh 1 --addSourceMeshExport $scaledFile #--invertNormal

#restore
scaleXyz.sh 5 $scaledFib Fib.xyz

Splines -i $offFile -f Fib.xyz -o "$outFib"
