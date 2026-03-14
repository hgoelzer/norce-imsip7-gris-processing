#!/bin/bash
# Remap directory and file names

if [ "$#" -ne 2 ]; then
    echo "Illegal number of parameters. Need 2, 1:model 2:exp"
fi

# location of Archive
outp=/projects/NS8006K/users/heig/MIPS/PROTECT-GrIS/norce-ismip6-gris-processing/Models


# labs list
lab=NORCE
# models list
#model=CISM16-MAR39-p50
model=$1

## exp mapping 
inexp=$2
outexp=`./rename_cism2protect.sh ${inexp}`
echo "# Found " ${outexp}
if [ "$outexp" = "Error" ]; then
    echo 'Error: experiment name could not be resolved'
    exit 0
fi
##### 
echo  Remapping names 

indir=${outp}/${lab}/${model}/${inexp}/
outdir=${outp}/${lab}/${model}/${outexp}/
#echo ${indir}
#echo ${outexp}
# go into exp dir and rename all files
cd ${indir}
# Rename
rename ${inexp} ${outexp} *.nc

# Now rename the dir itself
mv ${indir} ${outdir}

