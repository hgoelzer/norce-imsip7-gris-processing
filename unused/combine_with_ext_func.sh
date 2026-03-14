#!/bin/bash
# Combine run with extension

#if [ "$#" -ne 2 ]; then
#    echo "Illegal number of parameters. Need 2, 1:model 2:exp"
#fi

# location of Archive
outp=/projects/NS8006K/users/heig/MIPS/PROTECT-GrIS/norce-ismip6-gris-processing/Models


# labs list
lab=NORCE
# models list
#model=CISM04e-MAR312-p50
model=$1

## exp mapping 
#inexp=IPSL-CM6A-LR_ssp585_MARv3.12_p50
inexp=$2
#inexp_ext=IPSL-CM6A-LR_ssp585_MARv3.12_p50_ext
inexp_ext=$3
#outexp=IPSL-CM6A-LR_ssp585-e2200_MARv3.12_p50
outexp=$4

##### 
echo  Combining 

indir=${outp}/${lab}/${model}/${inexp}/
indir_ext=${outp}/${lab}/${model}/${inexp_ext}/
outdir=${outp}/${lab}/${model}/${outexp}/

mkdir ${outdir}
cd ${outdir}

ncs=`ls $indir | grep .nc`
for nc in $ncs; do
    echo Appending ext for ${nc} 
    ncrcat -O ${indir}/${nc} ${indir_ext}/${nc} ${outdir}/${nc} 
done
