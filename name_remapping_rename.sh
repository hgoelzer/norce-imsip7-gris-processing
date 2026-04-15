#!/bin/bash

set -x
set -e

# NORCE
outp=/nird/datapeak/NS5011K/users/heig/ISMIP7/norce-imsip7-gris-processing/Models/NORCE # Needs absolute path

models=`ls $outp | grep CISM`
echo $models

for model in $models; do
    echo $model
    
    ## processed
    apath=$outp/$model
    echo $apath
    
    cd ${apath}
    #rename "greenland_08km_v01_m08_r01_f85_fix" "exp01" *


    exps=`ls ${apath} | grep ^exp`
    for exp in $exps; do
	echo renaming in ${exp}
	cd ${apath}/${exp}
	rename "greenland_08km_v01_m08_r01_f85_fix" "exp01" *.nc

    done

done
