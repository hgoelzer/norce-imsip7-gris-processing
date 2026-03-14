#!/bin/bash
# Regrid a number of exps

# Doesn't always run smoothly with cdo throwing cdf errors and core.* files
# nird2 has been good so far
# Run repeatedly to catch all 

set -x
set -e

# source settings from python script
source setup_params.py

inpath=/nird/datapeak/NS5011K/users/heig/ISMIP7/norce-imsip7-gris-processing/proc/NORCE/${MODEL}

outpath=/nird/datapeak/NS5011K/users/heig/ISMIP7/norce-imsip7-gris-processing/Models/NORCE

echo $tier1_ID

# Parse exps from setup_params.py
exps=`echo $tier1_ID  | sed 's/,/ /g' | sed 's/\[/ /g' | sed 's/\]/ /g'`

for aexp in $exps; do
    # regrid fields
    echo $aexp
    ./regrid_exp_func.sh ${inpath} ${aexp} ${inres} ${outpath} ${MODEL} ${outres}    
done

