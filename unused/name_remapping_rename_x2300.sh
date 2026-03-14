#!/bin/bash

# NORCE
norce=/nird/projects/NS8006K/users/heig/MIPS/PROTECT-GrIS/norce-ismip6-gris-processing/Models/NORCE
# PROTECT archive
#norce=/nird/datalake/NS8085K/PROTECT-GrIS/Results/protect-gris-results-processing/Archive_sc/Data/SC_GIC1_OBS0/NORCE

models=`ls $norce | grep CISM16x-`
#models=`ls $norce | grep CISM04x-`

for model in $models; do
    echo $model
    
    ## processed
    apath=$norce/$model
    echo $apath
    
    cd ${apath}
    rename "ssp126_" "ssp126-x2300_" *
    rename "ssp585_" "ssp585-x2300_" *
    #rename "ctrl_proj" "ctrl_proj-x2300" *


    exps=`ls ${apath}`
    for exp in $exps; do
	echo renaming in ${exp}
	cd ${apath}/${exp}
	rename "ssp126_" "ssp126-x2300_" *
	rename "ssp585_" "ssp585-x2300_" *
	#rename "ctrl_proj" "ctrl_proj-x2300" *
	#rename "ctrl_proj" "ctrl-proj" *

    done

done
