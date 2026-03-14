#!/bin/bash

group=/nird/projects/NS8006K/users/heig/MIPS/PROTECT-GrIS/norce-ismip6-gris-processing/Models/NORCE

models=`cd $group ; find ./ -maxdepth 1 -mindepth 1 -type d;`
echo $models


for model in $models; do
    echo $model
    
    ## processed
    apath=$group/$model
    echo $apath
    #ls $apath
    
    cd ${apath}
#    rename "ACCESS1.6" "ACCESS1.3" *
#    rename "CESM2-CMIP6" "CESM2" *
#    rename "CNRM-CM6-1-1" "CNRM-CM6-1" *
#    rename "CNRM-ESM2-1-1" "CNRM-ESM2-1" *
#    rename "CSIRO-Mk3.6.0.0" "CSIRO-Mk3.6.0" *
#    rename "IPSL-CM5-MR" "IPSL-CM5A-MR" *
    rename "NorESM1-M-M" "NorESM1-M" *
    rename "NorESM2-MM-MM" "NorESM2-MM" *
#    rename "UKESM1-0-LL-CMIP6" "UKESM1-0-LL" *

    exps=`ls ${apath}`
    for exp in $exps; do
	echo renaming in ${exp}
	cd ${apath}/${exp}
#	rename "ACCESS1.6" "ACCESS1.3" *.nc
#	rename "CESM2-CMIP6" "CESM2" *.nc
#	rename "CNRM-CM6-1-1" "CNRM-CM6-1" *.nc
#	rename "CNRM-ESM2-1-1" "CNRM-ESM2-1" *.nc
#	rename "CSIRO-Mk3.6.0.0" "CSIRO-Mk3.6.0" *.nc
#	rename "IPSL-CM5-MR" "IPSL-CM5A-MR" *.nc
	rename "NorESM1-M-M" "NorESM1-M" *.nc
	rename "NorESM2-MM-MM" "NorESM2-MM" *.nc
#	rename "UKESM1-0-LL-CMIP6" "UKESM1-0-LL" *.nc
	
    done

done
